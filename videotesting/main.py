import os
import google.generativeai as genai

import cv2
import os
import shutil

SYSTEM_PROMPT = "Imagine the video given is from your perspective. Describe the scene, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you, in the last frame."
class File:
    def __init__(self, file_path: str, timestamp: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
            self.display_name = display_name
        self.timestamp = timestamp
    def set_response(self, response):
       self.response = response


class VideoGemini():
    def __init__(self, verbose: bool = False):
        key = os.environ["API_KEY"]
        genai.configure(api_key=key)
    
        self.file_path = os.path.dirname(os.path.realpath(__file__))

        self.video_path = f"{self.file_path}/videos/"

        self.model_1_5 = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        self.model_vision = genai.GenerativeModel(model_name="models/gemini-1.0-pro-vision")

        self.frames = []

        self.verbose = verbose

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
        self.frames.append(file)

    def _build_request(self):
        request = [SYSTEM_PROMPT]
        for frame in self.frames:
            request.append(frame.timestamp)
            request.append(frame.response)
        return request
    
    def get_response(self):
        # Make the LLM request.
        request = self._build_request()
        response = self.model.generate_content(request, request_options={"timeout": 600})
        return response

    def _delete_frames(self):
        if (self.verbose):
            print(f'Deleting {len(self.frames)} images. This might take a bit...')
        for frame in self.frames:
            genai.delete_file(frame.response.name)
            if (self.verbose):
                print(f'Deleted {frame.file_path} at URI {frame.response.uri}')
        if (self.verbose):
            print(f"Completed deleting files!\n\nDeleted: {len(self.frames)} files")

    def __del__(self):
        self._delete_frames()