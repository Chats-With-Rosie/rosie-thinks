import os
import subprocess
import requests
import base64

class ROS_Operator:

    def generate_valid_request(response):

        return valid_request

    def return_possible_ros_requests(self):
        

        possible_ros_requests = [
            "Rosie lift your arms",
            "Rosie please lift your arms",
            "Rosie, raise your arms",
            "Rosie, elevate your arms",
            "Rosie, lift up your arms",
            "Rosie, hoist your arms",
            "Rosie, pick up your arms",
            "Rosie, put your arms up",
            "Rosie, straighten your arms",
            "Rosie, reach for the sky",
            "Rosie, stretch your arms",
            "Rosie, extend your arms"
        ]
        return possible_ros_requests    
    
    def return_ros_requests(self):
        

        ros_requests = [
            "Rosie lift your arms",
            "Rosie untuck your arms",
            "Rosie tuck your arms",
            "Rosie enter sword fight mode",
        ]
        return ros_requests    


class send_to_agent:
    
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
    
    def send_string_to_endpoint(self, data_string,):
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