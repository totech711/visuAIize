import os
import google.generativeai as genai

import cv2
import os
import shutil
from gtts import gTTS
#SYSTEM_PROMPT = "Imagine the video given is from your perspective. Describe the scene, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you"

SYSTEM_PROMPT = "You are a viewing assistant for a blind person. Your job is to be their eyes, You will be given videos that represent the user's POV from the last 5 seconds. Provide a concise description, prioritizing nearby people, obstacles within a few steps, moving objects approaching us, and relevant environmental changes. Keep descriptions to one-two phrases.  Only provide descriptions when there are notable changes in the scene otherwise output <None> when you have already described the scene significantly. If anything is in reference to the camera, refer to the camera as 'you'"

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

        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest",  system_instruction=SYSTEM_PROMPT, 
        #         generation_config=genai.GenerationConfig(
        #     max_output_tokens = 100,
        #     temperature = 1.0
        # )
        )

        self.frames = []

        self.verbose = verbose

        self.delete = delete

        self.chat = self.model.start_chat(history=[])

    
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
    
    def increment_api_key(self):
        self.api_key_idx += 1
        self.api_key_idx = self.api_key_idx % len(self.api_keys)
        genai.configure(api_key=self.api_keys[self.api_key_idx])

    def get_response(self, query:str = None):
        if self.calls_this_min >= 2:
            self.api_key_idx += 1
            self.api_key_idx = self.api_key_idx % len(self.api_keys)
            genai.configure(api_key=self.api_keys[self.api_key_idx])
            self.calls_this_min = 0
        self.calls_this_min += 1
        print(f"gemini call api key is: {self.api_key_idx}")

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