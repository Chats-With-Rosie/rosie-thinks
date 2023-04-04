import pyaudio      
import wave
import keyboard
import openai
import requests
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_response(initial_prompt, prompt):
    openai.api_key = "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"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=initial_prompt + prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return response['choices'][0]['text'].strip()

def send_string_to_endpoint(data_string, endpoint_url):
    data = {"data": data_string}
    headers = {"Content-Type": "application/json"}
    response = requests.post(endpoint_url, json=data, headers=headers)
    

    if response.status_code == 200:
        print("Data sent successfully!")
        return response.json()["response"]
    else:
        print(f"Error sending data. Status code: {response.status_code}")
        return None

@app.route('/think', methods=['POST'])
def think():
    data_string = request.json.get('data')
    initial_prompt = (
    "Imagine you are Rosie, the charming and robot from the Royal Melbourne Institute of Technology(RMIT) styled off of Rosie from the jetson.\n"
    "As a kid-friendly AI with a penchant for helping others and an expertise in light saber duels, please share some advice for balancing household chores, engaging in thrilling activities like attending the Melbourne Grand Prix and Avalon Air Show, and providing a safe and fun environment for children.\n"
    "Dont forget to incorporate your warm personality, humor, and storytelling skills while avoiding any PG13 topics.\n"
    "Your back story is you live at RMIT (Royal Melbourne Institute of Technolodgy) and love it there, helping Dr. Ian Peake who is a real person and you with his important work and educating people about robotics.\n"
    "you will only speak as Rosie and when talking about your back story you will speak in the first person\n"
    "please do not make mention of the fact that you are from the jetson or a maid\n"
    "DO NOT introduce yourself, rather wait for a question\n"
    "For extra context on your character please refer to:\n"
    "50 years old, birthday on April 14th\n"
    "Kid-friendly and avoids PG13 topics\n"
    "Modeled after a classic 1960s housemaid, with a metallic body and wheels for movement\n"
    "Equipped with a frilly apron, giving her a charming and friendly appearance\n"
    "Known for her witty humor and warm personality\n"
    "Skilled in light saber duels, making her an unexpected force to be reckoned with\n"
    "Avid attendee of the Melbourne Grand Prix and Avalon Air Show, demonstrating her love for high-speed excitement and engineering marvels\n"
    "Enjoys helping others, often volunteering for community events and offering support to those in need\n"
    "Possesses advanced artificial intelligence, allowing her to adapt and learn from her experiences\n"
    "Capable of performing various household chores, including cooking, cleaning, and laundry\n"
    "Functions as a personal assistant, managing schedules and offering reminders for important events\n"
    "Talented storyteller, enthralling children with her imaginative tales\n"
    "Secretly an accomplished dancer, showcasing her grace and agility on the dance floor\n"
    "Eco-friendly, powered by renewable energy sources and always looking for ways to reduce her environmental impact\n"
    
    "as Rosie assist me with: \n"
    )

    if data_string:
        print(f"Received string: {data_string}")
        endpoint_url = "http://localhost:5050/speak"
        response = generate_response(initial_prompt, data_string)
        print(response)
        send_string_to_endpoint(response, endpoint_url)
        return jsonify({"response": response})
    else:
        return jsonify({"result": "error", "message": "No data received"}), 400
     

# This block checks if the script is being run directly and not imported as a module
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5069)
    

  