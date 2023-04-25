import pyaudio
import wave
import keyboard
import openai
import requests
import os
from flask import Flask, request, jsonify
from big_brain import Rosies_Big_Brain
from little_brain import Rosies_Little_Brain
from visualiser import Image_Generator 
from send_to_speak import send_to_speak# Don't forget to import LittleBrain
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
pre_prompt = None
little_brain_instance = None
big_brain_instance = None
dot_point_list = None
questions_list = None
model = None



def read_context_file(file_location):
    with open(file_location, "r") as file:
        file_contents = file.read()
    return file_contents


def is_question_similar(new_question, question_list, threshold=0.7):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Get embeddings for the new question and the existing questions
    new_question_embedding = model.encode(new_question)
    question_list_embeddings = model.encode(question_list)

    # Calculate cosine similarity between the new question and each question in the list
    similarities = cosine_similarity([new_question_embedding], question_list_embeddings)

    # Check if any similarity is above the threshold
    for similarity_value in similarities[0]:
        print(similarity_value)
        if similarity_value > threshold:
            return True
    return False

def check_string_in_list(lst, s):
    for item in lst:
        if item in s:
            return True
    return False
 

def generate_pre_prompt(context, pre_prompt_file, context_file):

    big_brain = Rosies_Big_Brain(api_key, speak_endpoint)
    
    print("#####################PRE-PROMPT#####################")
   
    pre_prompt = big_brain.big_brain_message_start_up_refine_context(context, context_file,2500, 0.1)
    print(pre_prompt)
    refined_prompt = refined_prompt = big_brain.big_brain_generate_context_prompt(pre_prompt, pre_prompt_file,2500, 0.1)
    print(refined_prompt)
    print("#####################END OF PRE-PROMPT#####################")
    if refined_prompt:
        return refined_prompt
    else:
        return None

def start_up(file_name, file_location, speak_endpoint, api_key):
    print("#####################START-UP#####################")
    print("#####################START OF CONTEXT#####################")
    speak_sender = send_to_speak(speak_endpoint)
    speak_sender.send_string_to_endpoint("Loading Context")
    context = read_context_file(file_name)
    print(context)
    print("#####################END OF CONTEXT#####################")
    
    pre_prompt_file = os.path.join(file_location, 'pre-prompt.txt')
    context_file = os.path.join(file_location, 'shotened-context.txt')
    speak_sender.send_string_to_endpoint("Generating Pre Prompt")
    pre_prompt = generate_pre_prompt(context, pre_prompt_file, context_file)
 
    
    print(pre_prompt)
    print("#####################END OF PRE-PROMPT#####################")
    speak_sender.send_string_to_endpoint("Training My Little Brain")
    little_brain = Rosies_Little_Brain(file_location, speak_endpoint)  # Create an instance of LittleBrain with the context
    big_brain = Rosies_Big_Brain(api_key, speak_endpoint)
    dot_point_context_file = os.path.join(file_location, 'dot-point-context.txt')
    python_list = little_brain.get_context_as_python_list(context,dot_point_context_file)
    
    
    print(dot_point_list)
    question_file = os.path.join(file_location, 'question-context.txt')
    questions_list = little_brain.ask_questions_and_get_responses(python_list, question_file)
    model = little_brain.train_model(file_location)

    return pre_prompt, little_brain, big_brain, dot_point_list, questions_list, model


@app.route('/think', methods=['POST'])
def think():
    global pre_prompt
    global little_brain_instance
    global big_brain_instance
    global dot_point_list
    global questions_list
    global model
    print("little brain questions list")
    print(questions_list)
    data_string = request.json.get('data')
    api_key = os.environ.get('OPENAI_API_KEY')
    generator = Image_Generator("images/my_generated_image.jpg",api_key)
    image_generation_questions = generator.return_image_requests()
    if data_string:
        if check_string_in_list(data_string, questions_list) or is_question_similar(data_string, questions_list):
            print("Is a little brian question")
            print(little_brain_instance.extract_answer_from_files("context-folder/", data_string))
            speak_sender = send_to_speak(speak_endpoint)
            speak_sender.send_string_to_endpoint(little_brain_instance.extract_answer_from_files("context-folder/", data_string))
            return little_brain_instance.ask_little_brain_a_question(model, data_string)
        elif check_string_in_list(data_string, image_generation_questions) or is_question_similar(data_string, image_generation_questions, 0.5):
            speak_sender = send_to_speak(speak_endpoint)
            speak_sender.send_string_to_endpoint("Hmmmmm, bare with whilst I work my magic!")
            generated = generator.generate_image_from_prompt(data_string)
            generator.open_image_file()
            speak_sender.send_string_to_endpoint("Here you go... What do you think?")
            return generated 
        else:
            return big_brain_instance.ask_big_brain(2700, 0.8, message="", user_message_content=data_string, pre_prompt=pre_prompt)


if __name__ == '__main__':
    speak_endpoint = 'http://localhost:5050/speak'
    api_key = os.environ.get('OPENAI_API_KEY')
    pre_prompt, little_brain_instance, big_brain_instance, dot_point_list, questions_list, model = start_up("context-folder/context.txt", "context-folder/", speak_endpoint, api_key)
    app.run(host='0.0.0.0', port=5869, debug=True)
