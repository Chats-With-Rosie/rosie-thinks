import pyaudio      
import wave
import keyboard
import openai
import requests
import os


openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Hello, what are your thoughts on critical race theory?",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)

print (response['choices'][0]['text'])