import os
import google.generativeai as genai

import cv2
import os
import shutil
import asyncio

#SYSTEM_PROMPT = "Imagine the video given is from your perspective. Describe the scene, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you"

SYSTEM_PROMPT = "You are a viewing assistant for a blind person. Your job is to be their eyes, describe the scene when necessary, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you. Only include descriptions that are relevant to the blind person you are helping, for example obstacles that are close, people that are close, objects moving towards them, etc. All responses must be within one or two lines. Output <None> when you have already described the scene significantly."
class File:
    def __init__(self, file_path: str, timestamp: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
            self.display_name = display_name
        self.timestamp = timestamp
    def set_response(self, response):
       self.response = response
from datetime import datetime
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
    
    async def get_response_async(self):
        request = self._build_request()
        resp = self.chat.send_message(request)
        print(resp.text)
    
    def get_response(self, query:str = None):
        if (self.calls_this_min >= 2):
            api_key_idx += 1
            api_key_idx = api_key_idx % len(self.api_keys)
            self.calls_this_min = 0
        self.calls_this_min += 1
            
        # Make the LLM request.
        request = self._build_request(query)
        response = ""
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

"""class ImageGemini():
    def __init__(self, verbose: bool = False, delete: bool = True):
        key = os.environ["API_KEY"]
        genai.configure(api_key=key)
    
        self.file_path = os.path.dirname(os.path.realpath(__file__))

        self.video_path = f"{self.file_path}/videos/"

        self.model = genai.GenerativeModel(model_name="models/gemini-1.0-pro-vision")

        self.frame = None

        self.verbose = verbose

        self.delete = delete

    def upload_frame(self, file: File):
        if (self.verbose):
            print(file.file_path)
            print(f'Uploading: {file.file_path}...')
        response = genai.upload_file(path=file.file_path)
        file.set_response(response)
        if (self.verbose):
            print(f"Completed file upload")
            print(f"Deleting local file at {file.file_path}")

        os.remove(file.file_path)
        file.file_path = ""
        self.frame = file

    def _build_request(self):
        request = [SYSTEM_PROMPT]
        request.append(self.frame.response)
        return request
    
    def get_response(self):
        # Make the LLM request.
        request = self._build_request()
        response = ""
        response = self.model.generate_content(request, request_options={"timeout": 600})
        return response

    def _delete_frames(self):
        if (self.verbose):
            print(f'Deleting image. This might take a bit...')
        genai.delete_file(self.frame.response.name)
        if (self.verbose):
            print(f'Deleted {self.frame.file_path} at URI {self.frame.response.uri}')
        if (self.verbose):
            print(f"Completed deleting files!\n\nDeleted file")

    def __del__(self):
        if (self.delete):
            self._delete_frames()"""
if (__file__ == "__main__"):
    ai = ImageGemini(True)
    file_path = os.path.dirname(os.path.realpath(__file__))
    FRAME_EXTRACTION_DIRECTORY = file_path + "/content/frames"

    f = File(f"{FRAME_EXTRACTION_DIRECTORY}/IMG_2946_MOV_frame00:01.jpg", None)
    ai.upload_frame(f)
    resp = ai.get_response()
    print(resp)