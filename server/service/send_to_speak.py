import requests 
import base64

class send_to_speak:
    # A class for managing sending of string and image data to specified endpoints.

    
    def __init__(self, endpoint_url,image_endpoint_url=""):
        #Initializes the instance with the provided endpoint URLs for string and image data.

        self.endpoint_url = endpoint_url
        self.image_endpoint_url = image_endpoint_url
    
    def send_string_to_endpoint(self, data_string, thinking=True):
        #Sends the provided string data to the endpoint URL and returns the response.

        data = {"data": data_string}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.endpoint_url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("Data sent successfully!")
            print(f"Response content: {response.content}")  # Add this line to print the response content
            return response.json()["response"]
        else:
            print(f"Error sending data. Status code: {response.status_code}")
            return None
        
    def send_image_to_endpoint(self, image_location):
        #Sends the image file located at the provided path to the image endpoint URL and returns the response.
        with open(image_location, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data = {"image": encoded_image}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.image_endpoint_url, json=data, headers=headers)

        response_json = response.json()
        if response.status_code == 200 and "response" in response_json:
            print("Image sent successfully!")
            print(f"Response content: {response.content}")
            return response_json["response"]
        elif "error" in response_json:
            print(f"Error sending image: {response_json['error']}")
        else:
            print(f"Error sending image. Status code: {response.status_code}")
        return None
