'''import PIL.Image
import os

import google.generativeai as genai

key1 = os.environ["API_KEY"]
key2 = os.environ["API_KEY2"]

genai.configure(api_key=key1)

SYSTEM_PROMPT = "Say Hello!"
SYSTEM_PROMPT = "Say Bye!"
SYSTEM_PROMPT = "Say Hola!"
SYSTEM_PROMPT = "Say red!"

genai.configure(api_key=key2)

SYSTEM_PROMPT = "what was the second thing I asked"

model = genai.GenerativeModel('gemini-pro-vision')
'''

import os
import google.generativeai as genai

key1 = os.environ["API_KEY"]
key2 = os.environ["API_KEY2"]

genai.configure(api_key=key1)

SYSTEM_PROMPTS = ["Explain what a black hole is", "Whats your favorite thing", "What did I just ask?", "Bye"]

responses = []
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
chat = model.start_chat(history=[])

for prompt in SYSTEM_PROMPTS[:2]:
    print("here")
    response = chat.send_message(prompt)
    responses.append(response.text)

# Now, you can access the responses based on the order of prompts
print("Responses:", responses)

# Now configure with the second API key
genai.configure(api_key=key2)

# Asking a question about the history
query = "What is the first thing I asked?"
response_to_query = chat.send_message(query)
print("Response to query:", response_to_query.text)
