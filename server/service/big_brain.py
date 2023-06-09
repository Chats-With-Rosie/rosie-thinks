import openai;
from send_to_speak import send_to_speak;
import logging;
import os
import json


class Rosies_Big_Brain:
    
    #A class to interact with OpenAI's GPT model to refine text contexts, generate prompts, and send refined messages. 
    #Also supports logging and storing results to a file.
    

    def __init__(self, api_key, speak_endpoint):

        #Initializes the instance with provided api_key and speak_endpoint. Also sets up logging.

        self.api_key = api_key
        self.speak_endpoint = speak_endpoint
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)


    def big_brain_message_start_up_refine_context(self, context, file_path, tokens, temperature):
        #Reads context from file, refines it with AI, writes the refined context back to file and logs the process.

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                refined_context = f.read()
        else:
            message = [
                {
                    "role": "system",
                    "content": "You are an AI language model. Please process, shorten, contextualize, and improve the following text. Then, based on the improved text, suggest personality traits for a kid-friendly robot. Finally, create a prompt that instructs an AI language model to behave like the given character, DO NOT REQUEST ANYTHING OF THE CHARACTER, THE CHARACTER IS AT AN AI CONVENTION:"
                },
                {
                    "role": "user",
                    "content": f"Text:\n\n{context}"
                }
            ]
            refined_context = self.ask_big_brain(tokens, temperature, message)
            with open(file_path, 'w') as f:
                f.write(refined_context)
            self.logger.info(f'Refined Context: {refined_context}')

        return refined_context


    def big_brain_generate_context_prompt(self, refined_context, file_path,tokens, temperature):
        #Reads refined context from file, generates a prompt with AI, writes the prompt back to file, and logs the process.

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                pre_prompt = f.read()
        else:
            message = [
                {
                    "role": "system",
                    "content": "You are an expert at creating prompts that enable ai models like gpt-3.5 to behave like a certain character, you will be given context and you will refine it to a prompt that maintains the same structure as: you are (character) whenever you are addressed you will respond as (character) and in the first person, you will keep your responses short and to the point and you character has the following characteristics, (characteristics), as (character) assist me with"
                },
                {
                    "role": "user",
                    "content": f"please create a prompt based off of the following informations, reply with nothing but the refined prompt no other writing is necessary, please end all prompts with 'as (character) assist me with:' ::\n\n{refined_context}"
                }
            ]

            pre_prompt = self.ask_big_brain(tokens, temperature, message)
            with open(file_path, 'w') as f:
                f.write(pre_prompt)
            self.logger.info(f'Pre Prompt: {pre_prompt}')

        return pre_prompt
    def big_brain_message(self, message, user_message_content, pre_prompt=""):
        #Returns a formatted message with a pre_prompt and user_message_content.

        if len(pre_prompt) > 3:
            message = [
                {
                    "role": "system",
                    "content": f"{pre_prompt}:"
                },
                {
                    "role": "user",
                    "content": f"As Rosie assist me with:\n\n{user_message_content}"
                }
            ]
            return message
        else:
            return message
        
    def append_dictionary_to_file(self, file_path, dictionary):
        #Appends a dictionary to a file in JSON format.

        try:
            with open(file_path, 'a') as file:
                file.write(json.dumps(dictionary))
                file.write('\n')
            print(f"Dictionary appended to {file_path}")
        except Exception as e:
            print(f"Error while appending dictionary to file: {e}")

    def ask_big_brain(self, tokens, temperature, message = "", user_message_content = "" ,pre_prompt = ""):
        
        # Communicates with the OpenAI GPT model to generate responses, logs the response to an endpoint, and saves the results to a file.

        
        speak_sender = send_to_speak(self.speak_endpoint)
        speak_sender.send_string_to_endpoint("Hmmmmm, let me think about that for a second!")
        
        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=self.big_brain_message(message ,user_message_content, pre_prompt),
        max_tokens=tokens,
        n=1,
        temperature=temperature,    
        )
        print(response)  
        speak_sender.send_string_to_endpoint(response['choices'][0]['message']['content'].strip())

        string_response = response['choices'][0]['message']['content'].strip()

        result = {
        "Prompt": user_message_content,
        "Completion": string_response
        }
        self.append_dictionary_to_file("big_brain_results.json", result)
        return response['choices'][0]['message']['content'].strip()

