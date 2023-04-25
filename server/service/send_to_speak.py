import requests 

class send_to_speak:
    
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
    
    def send_string_to_endpoint(self, data_string, thinking=True):
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
