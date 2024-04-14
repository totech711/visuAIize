import os
import google.generativeai as genai


import cv2
import os
import shutil
from gtts import gTTS
#SYSTEM_PROMPT = "Imagine the video given is from your perspective. Describe the scene, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you"


SYSTEM_PROMPT = "You are a viewing assistant for a blind person. Your job is to be their eyes, Provide a concise description, prioritizing nearby people, obstacles within a few steps, moving objects approaching us, and relevant environmental changes. Keep descriptions to one-two phrases and only update when there are changes or upon request.  Output <None> when you have already described the scene significantly. Summarize only the frames provided in 10 words maximum only. If anything is in reference to the camera, refer to the camera as 'you'"


class File:
   def __init__(self, file_path: str, timestamp: str, display_name: str = None):
       self.file_path = file_path
       if display_name:
           self.display_name = display_name
       self.timestamp = timestamp
   def set_response(self, response):
       self.response = response


class VideoGemini():
   def __init__(self, api_keys: list[str], verbose: bool = False, delete: bool = True):
       #api key switching logic
       self.api_keys = api_keys
       self.api_key_idx = 0
       self.calls_this_min = 0


       genai.configure(api_key=api_keys[self.api_key_idx])


       self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest",  system_instruction=SYSTEM_PROMPT)


       self.frames = []


       self.verbose = verbose


       self.delete = delete


       self.chat = self.model.start_chat(history=[])


      
   async def async_upload_frame(self, file: File):
       if (self.verbose):
           print(file.file_path)
           print(f'Uploading: {file.file_path}...')
       response = genai.upload_file(path=file.file_path)
       file.set_response(response)
       if (self.verbose):
           print(f"Completed file upload")
           if (self.delete):
               print(f"Deleting local file at {file.file_path}")
       if (self.delete):
           os.remove(file.file_path)
           file.file_path = ""
       self.frames.append(file)


   def upload_frame(self, file: File):
       if (self.verbose):
           print(file.file_path)
           print(f'Uploading: {file.file_path}...')
       response = genai.upload_file(path=file.file_path)
       file.set_response(response)
       if (self.verbose):
           print(f"Completed file upload")
           if (self.delete):
               print(f"Deleting local file at {file.file_path}")
       if (self.delete):
           os.remove(file.file_path)
           file.file_path = ""
       self.frames.append(file)


   def _build_request(self, query:str = None):
       request = []
       if (query):
           request.append(query)
       for frame in self.frames:
           request.append(frame.timestamp)
           request.append(frame.response)
       return request
  
   async def async_get_response(self, query:str = None):
       if (self.calls_this_min >= 2):
           self.api_key_idx += 1
           self.api_key_idx = self.api_key_idx % len(self.api_keys)
           self.calls_this_min = 0
       self.calls_this_min += 1
          
       # Make the LLM request.
       request = self._build_request(query)
       response = self.chat.send_message(request)
       self.frames = []
       return (response.text.replace("<None>", ""))


   def get_response(self, query:str = None):
       print(f"gemini call api key is: {self.api_key_idx}")
       if (self.calls_this_min >= 2):
           self.api_key_idx += 1
           self.api_key_idx = self.api_key_idx % len(self.api_keys)
           self.calls_this_min = 0
       self.calls_this_min += 1
       dir_path = os.path.dirname(os.path.realpath(__file__))
          
       # Make the LLM request.
       request = self._build_request(query)
       response = self.chat.send_message(request)
       return response


   def _delete_frames(self):
       if (self.verbose):
           print(f'Deleting {len(self.frames)} images. This might take a bit...')
       for frame in self.frames:
           print("here")
           genai.delete_file(frame.response.name)
           print('here2')
           if (self.verbose):
               print(f'Deleted {frame.file_path} at URI {frame.response.uri}')
       if (self.verbose):
           print(f"Completed deleting files!\n\nDeleted: {len(self.frames)} files")
   def __del__(self):
       self._delete_frames()

