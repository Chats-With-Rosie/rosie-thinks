from diffusers import StableDiffusionPipeline
import torch
import os
import subprocess
import requests
import openai


class Image_Generator:
    def __init__(self,output_file_path, api_key):
        self.output_file_path = output_file_path
        self.api_key = api_key
    
    def send_image_to_endpoint(self, image_filename, endpoint_url):
        image_filepath = os.path.join('images', image_filename)  # Update this with the correct path to your image files

        if not os.path.exists(image_filepath):
            print("Error: image file not found.")
            return None

        with open(image_filepath, 'rb') as image_file:
            files = {'file': (image_filename, image_file, 'image/jpeg')}  # Update the content type if you're using a different image format
            response = requests.post(endpoint_url, files=files)

        if response.status_code == 200:
            print("Image file sent successfully!")
            print(f"Response content: {response.content}")  # Add this line to print the response content
            return response.json()["response"]
        else:
            print(f"Error sending image file. Status code: {response.status_code}")
            return None
        
    def generate_image_from_prompt(self, prompt):
        
        openai.api_key = self.api_key

        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="256x256",
            )

            image_url = response['data'][0]['url']
            image_data = requests.get(image_url).content

            with open(self.output_file_path , 'wb') as output_file:
                output_file.write(image_data)
            print(f"Image saved at {self.output_file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def open_image_file(self):
        if os.path.exists(self.output_file_path):
            endpoint_url = os.environ.get('FRONT_END_IMAGE_URL')
            self.send_image_to_endpoint(self.output_file_path, endpoint_url)
            if os.name == 'nt':  # for Windows
                os.startfile(self.output_file_path)
            elif os.name == 'posix':  # for Mac and Linux
                subprocess.call(['open', self.output_file_path])
        else:
            print(f"Error: Could not find image file at {self.output_file_path}")
    
    def return_image_requests(self):
   

        image_requests = [
            "Rosie, generate an image of",
            "Rosie, show me an image of",
            "Rosie, create an image of",
            "Rosie, produce an image of",
            "Rosie, display an image of",
            "Rosie, make an image of",
            "Rosie, craft an image of",
            "Rosie, design an image of",
            "Rosie, generate a picture of",
            "Rosie, create a visual of",
            "Rosie, fetch me an image of",
            "Rosie, search for an image of",
            "Rosie, find me a picture of",
            "Rosie, get me a visual of",
            "Rosie, illustrate an image of",
            "Rosie, render an image of",
            "Rosie, generate a graphic of",
            "Rosie, draw me an image of",
            "Rosie, present an image of",
            "Rosie, capture an image of",
            "Rosie, conjure an image of",
            "Rosie, compose a picture of",
            "Rosie, sculpt an image of",
            "Rosie, formulate a visual of",
            "Rosie, design a graphic of",
            "Rosie, fabricate an image of",
            "Rosie, draft an image of",
            "Rosie, originate an image of",
            "Rosie, dream up an image of",    
            "Generate an image of",
            "Show me an image of",
            "Create an image of",
            "Produce an image of",
            "Display an image of",
            "Make an image of",
            "Craft an image of",
            "Design an image of",
            "Generate a picture of",
            "Create a visual of",
            "Fetch me an image of",
            "Search for an image of",
            "Find me a picture of",
            "Get me a visual of",
            "Illustrate an image of",
            "Render an image of",
            "Generate a graphic of",
            "Draw me an image of",
            "Present an image of",
            "Capture an image of",
            "Conjure an image of",
            "Compose a picture of",
            "Sculpt an image of",
            "Formulate a visual of",
            "Design a graphic of",
            "Fabricate an image of",
            "Draft an image of",
            "Originate an image of",
            "Dream up an image of"
        ]
        return image_requests
