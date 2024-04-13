import PIL.Image
import os

import google.generativeai as genai

key = os.environ["API_KEY"]
SYSTEM_PROMPT = "Imagine the image given is from your perspective. Describe the scene, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you. Do not make anything up, just simply state what is happening."

genai.configure(api_key=key)

file_path = os.path.dirname(os.path.realpath(__file__))
FRAME_EXTRACTION_DIRECTORY = file_path + "/content/frames/"

img = PIL.Image.open(FRAME_EXTRACTION_DIRECTORY + "IMG_2946_MOV_frame00:00.jpg")

model = genai.GenerativeModel('gemini-pro-vision')

from datetime import datetime
print(datetime.now())
response = model.generate_content([SYSTEM_PROMPT, img])
print(datetime.now())

print(response.text)