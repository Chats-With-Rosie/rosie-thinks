import wave
import openai
import os
from flask import Flask, request
from big_brain import Rosies_Big_Brain
from little_brain import Rosies_Little_Brain
from visualiser import Image_Generator 
from send_to_speak import send_to_speak# Don't forget to import LittleBrain
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initializes a Flask application
app = Flask(__name__)

# Global variables to hold values that need to be accessible throughout the application
pre_prompt = None
little_brain_instance = None
big_brain_instance = None
dot_point_list = None
questions_list = None

model = None # Placeholder for a SentenceTransformer model
CONTEXT_FOLDER = 'context-folder'   # Folder where context files are stored
CONTEXT_FILE = 'context.txt' # File where context text is stored


def write_context_file(data): # Writes data to the context file
    context_file_path = os.path.join(CONTEXT_FOLDER, CONTEXT_FILE)
    with open(context_file_path, 'w') as f:
        f.write(data)


def read_context_file(file_location):  # Reads the contents of a file
    with open(file_location, "r") as file:
        file_contents = file.read()
    return file_contents


def is_question_similar(new_question, question_list, threshold=0.7):   # Checks if a question is similar to others in a list
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

def check_string_in_list(lst, s):   # Checks if a string is in a list of strings
    for item in lst:
        if item in s:
            return True
    return False
 

def generate_pre_prompt(context, pre_prompt_file, context_file):  # Generates a pre-prompt using the "big brain"

    big_brain = Rosies_Big_Brain(api_key, speak_endpoint)
    
    print("#####################PRE-PROMPT#####################")
   
    pre_prompt = big_brain.big_brain_message_start_up_refine_context(context, context_file,1800, 0.1)
    print(pre_prompt)
    refined_prompt = refined_prompt = big_brain.big_brain_generate_context_prompt(pre_prompt, pre_prompt_file,1800, 0.1)
    print(refined_prompt)
    print("#####################END OF PRE-PROMPT#####################")
    if refined_prompt:
        return refined_prompt
    else:
        return None

def start_up(file_name, file_location, speak_endpoint, api_key):  # Starts the application, initializing the "little brain" and "big brain"
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
    
    question_file = os.path.join(file_location, 'question-context.txt')
    questions_list = little_brain.ask_questions_and_get_responses(python_list, question_file)
    

    return pre_prompt, little_brain, big_brain, dot_point_list, questions_list

@app.route('/think', methods=['POST'])
def think():  # Endpoint that receives data to think about and determines where to send it for processing
    global pre_prompt
    global little_brain_instance
    global big_brain_instance
    global dot_point_list
    global questions_list
    print("little brain questions list")
    print(questions_list)
    data_string = request.json.get('data')
    api_key = os.environ.get('OPENAI_API_KEY')
    generator = Image_Generator("images/my_generated_image.jpg",api_key)
    image_generation_questions = generator.return_image_requests()
    if data_string:
        if check_string_in_list(data_string, questions_list) or is_question_similar(data_string, questions_list, 0.6):
            print("Sent to little brain")
            speak_sender = send_to_speak(speak_endpoint)
            response = little_brain_instance.extract_answer_from_files("context-folder/", data_string)
            speak_sender.send_string_to_endpoint(response)
            print(response)
            return 
        elif check_string_in_list(data_string, image_generation_questions) or is_question_similar(data_string, image_generation_questions, 0.5):
            speak_sender = send_to_speak(speak_endpoint,os.environ.get('FRONT_END_IMAGE_UPLOAD') or "http://frontend:5050/upload-image")
            speak_sender.send_string_to_endpoint("Hmmmmm, bare with me whilst I work my magic!")
            generated = generator.generate_image_from_prompt(data_string)
            generator.open_image_file()
            speak_sender.send_string_to_endpoint("Here you go... What do you think?")
            return generated 
        else:
            return big_brain_instance.ask_big_brain(700, 0.8,message="", user_message_content=data_string, pre_prompt=pre_prompt)

@app.route('/upload-context', methods=['POST'])
def upload():  # Endpoint that receives and updates the context
    data = request.get_data(as_text=True)
    write_context_file(data)
    
    return 'Context updated'


if __name__ == '__main__':
    speak_endpoint = os.environ.get('SPEAK_SERVICE') or 'http://speak_service:5050/rosie-speak'
    api_key = os.environ.get('OPENAI_API_KEY')
    pre_prompt, little_brain_instance, big_brain_instance, dot_point_list, questions_list = start_up("context-folder/context.txt", "context-folder/", speak_endpoint, api_key)
    app.run(host='0.0.0.0', port=5080)
