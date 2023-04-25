import os
import subprocess
import requests
import openai


class Image_Generator:
    def __init__(self,output_file_path, api_key):
        self.output_file_path = output_file_path
        self.api_key = api_key
    
    def send_image_url_to_endpoint(self, image_url, endpoint=os.environ.get('FRONT_END_IMAGE_UPLOAD') or 'http://frontend:5069/upload'):
        data = {"image_url": image_url}
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, json=data, headers=headers)

        if response.status_code == 200:
            print("Image URL sent successfully!")
            print(f"Response content: {response.content}")
        else:
            print(f"Error sending image URL. Status code: {response.status_code}")

        
    def generate_image_from_prompt(self, prompt):
        
        openai.api_key = self.api_key

        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="256x256",
            )

            image_url = response['data'][0]['url']
            self.send_image_url_to_endpoint(image_url)
            image_data = requests.get(image_url).content

            with open(self.output_file_path , 'wb') as output_file:
                output_file.write(image_data)
            print(f"Image saved at {self.output_file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def open_image_file(self):
        if os.path.exists(self.output_file_path):
            if os.name == 'nt':  # for Windows
                os.startfile(self.output_file_path)
            elif os.name == 'posix':  # for Mac and Linux
                subprocess.call(['open', self.output_file_path])
        else:
            print(f"Error: Could not find image file at {self.output_file_path}")
    
    def return_image_requests(self):
   

        image_requests = [
            "generate an image of",
            "show me an image of",
            "create an image of",
            "produce an image of",
            "display an image of",
            "make an image of",
            "craft an image of",
            "design an image of",
            "generate a picture of",
            "create a visual of",
            "fetch me an image of",
            "search for an image of",
            "find me a picture of",
            "get me a visual of",
            "illustrate an image of",
            "render an image of",
            "generate a graphic of",
            "draw me an image of",
            "present an image of",
            "capture an image of",
            "conjure an image of",
            "compose a picture of",
            "sculpt an image of",
            "formulate a visual of",
            "design a graphic of",
            "fabricate an image of",
            "draft an image of",
            "originate an image of",
            "dream up an image of",    
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
