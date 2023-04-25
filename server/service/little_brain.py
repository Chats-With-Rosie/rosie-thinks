#context needs to be provided and created.
#can scrape the data from the web and create the context
#I think because we need to have questions as well as answers it makes sense to use some hugging face models
#I think we can load the hugging face model with context
#use a questions answerer to get the answer
import openai
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import requests
from sentence_transformers import SentenceTransformer
import json
import random
import json
import random
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
import os
from pprint import pprint;
import haystack;
from haystack.document_stores import InMemoryDocumentStore;
from haystack.nodes import BM25Retriever, FARMReader;
from haystack.pipelines import ExtractiveQAPipeline;
from haystack.pipelines.standard_pipelines import TextIndexingPipeline;
from haystack.utils import fetch_archive_from_http;
from send_to_speak import send_to_speak;
from big_brain import Rosies_Big_Brain;
from transformers import T5ForConditionalGeneration, T5Tokenizer;

class Rosies_Little_Brain:

    def __init__(self, context_file, speak_endpoint):
        self.context_file = context_file
        self.speak_endpoint = speak_endpoint
        self.tokenizer = AutoTokenizer.from_pretrained("voidful/context-only-question-generator")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("voidful/context-only-question-generator")



    
    def append_to_file(self,text, file_location):
        with open(file_location, 'a') as file:
            file.write(text)

    def extract_context_from_file(self, file_path):
        with open(file_path, 'r') as f:
            context = f.read()
        return context

    def return_summry_of_context(self, context):
        context_list = self.paginate_text(context)
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary_list = []
        for context in context_list:
            summary = summarizer(context, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            summary_list.append(summary)
        return summary_list


    def return_context_as_list(self, context):
        message = [
        {
            "role": "system",
            "content": "You are a helpful assistant and an expert in returning python lists. Your current task is to convert the provided information into a well formatted python list. Each item in the list should be a complete sentence, and the list should be returned as a list of strings. Please ensure that the list is easy to understand and that it accurately conveys the meaning of the original information. DO NOT RETURN ANYTHING OTHER THAN THE LIST IN []."
        },
        {
            "role": "user",
            "content": f"{context}"
        }
        ]
        speak_endpoint = 'http://localhost:5050/speak'
        api_key = os.environ.get('OPENAI_API_KEY')
        big_brain = Rosies_Big_Brain( api_key, speak_endpoint)
        
        output = big_brain.ask_big_brain(3250, 0.2, message=message, user_message_content = "" ,pre_prompt = "")
        return output

    def train_model(self, local_data_dir: str):
        logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
        logging.getLogger("haystack").setLevel(logging.INFO)

        document_store = InMemoryDocumentStore(use_bm25=True)

        files_to_index = [local_data_dir + "/" + f for f in os.listdir(local_data_dir)]
        indexing_pipeline = TextIndexingPipeline(document_store)
        indexing_pipeline.run_batch(file_paths=files_to_index)

        retriever = BM25Retriever(document_store=document_store)
        reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

        pipe = ExtractiveQAPipeline(reader, retriever)
        
        return pipe 

    def ask_little_brain_a_question(self, pipe, question: str):
        prediction = pipe.run(
            query=question,
            params={
                "Retriever": {"top_k": 10},
                "Reader": {"top_k": 5}
            }
        )

        # Check if the 'answers' key exists and if it contains at least one answer
        if "answers" in prediction and len(prediction["answers"]) > 0:
            # Access the first answer in the list (assuming it's an 'Answer' object)
            answer = prediction["answers"][0]

            # Access the 'answer' attribute if it exists in the 'Answer' object
            if hasattr(answer, "answer"):
                speak_sender = send_to_speak(self.speak_endpoint)
                speak_sender.send_string_to_endpoint(answer.answer)
                return answer.answer
            else:
                return "No 'answer' attribute found in the 'Answer' object"
        else:
            return "No answers found"
        
    def extract_answer_from_files(directory_path: str, question: str):
        # Initialize the question-answering pipeline
        question_answerer = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        
        # Read all files in the directory and combine their content
        context = ""
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    context += file.read() + "\n"

        # Get the answer to the question using the combined context
        result = question_answerer(question=question, context=context)
        
        # Return the answer
        return result['answer']

   

    
    def generate_question(self, context):
        print("##############################################")
        inputs = self.tokenizer(context, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(question)
        print("##############################################")
        return question
    
    def extract_list_from_string(self, lst_string):
        lst = lst_string.split("[")[1].split("]")[0]
        lst = lst.replace('"', '').split(",")
        lst = [item.strip() for item in lst]
        return lst
        
    def get_context_as_python_list(self, context, file_path):
        if isinstance(context, list):
            print("Input context is already a list!")
            return context

        while True:
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    context_as_list = f.read()
            else:
                context_as_list = self.return_context_as_list(context)
                with open(file_path, 'w') as f:
                    f.write(context_as_list)
            context_as_a_python_list = self.extract_list_from_string(context_as_list)
            if isinstance(context_as_a_python_list, list):
                print("Successfully extracted context as a list!")
                print(len(context_as_a_python_list))
                return context_as_a_python_list
            else:
                print("Error: context is not a valid list!")
                # handle the case where context_as_a_python_list is not a list
                continue
  
    def ask_questions_and_get_responses(self, contexts, file_location):
            responses = []

            if os.path.exists(file_location):
                with open(file_location, 'r') as file:
                    responses = json.load(file)
            else:
                for context in contexts:
                    try:
                        response_text = self.generate_question(context)
                        responses.append(response_text)
                    except Exception as e:
                        print(f"Error: {str(e)}")

                # Save responses to the file
                with open(file_location, 'w') as file:
                    json.dump(responses, file)

            return responses

# speak_endpoint = 'http://localhost:5050/speak'
# littlest_brain = Rosies_Little_Brain("context-folder/", speak_endpoint)
# model = littlest_brain.train_model("context-folder/")
# response = littlest_brain.ask_little_brain_a_question(model, question)