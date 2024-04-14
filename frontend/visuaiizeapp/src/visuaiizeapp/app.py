"""
Build the world around you for you
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga import Image, ImageView, Canvas
# import pygame 
# import pygame.camera 
from PIL import Image as img
from io import BytesIO
import os
import cv2
from time import sleep
from .geminidriver import *

from datetime import datetime
import asyncio
from gtts import gTTS
import playsound
from pydub import AudioSegment


class VisuAIizeApp(toga.App):
    main_box = toga.Box()
    def startup(self):
        key1 = os.environ["API_KEY1"]
        key2 = os.environ["API_KEY2"]
        self.ai = VideoGemini(api_keys=[key1, key2], verbose=True, delete=False)
        main_box = toga.Box()
        button = toga.Button(
            "START MY DAY",
            on_press=self.save_picture,
            style=Pack(padding=5)
        )

        main_box.add(
            toga.ImageView(
                
                style=Pack(flex=1, width=150),
            )
        )

        self.starting = datetime.now()
        self.cap = None

        #my_image = toga.Image("filename.png")
        #view = toga.ImageView(my_image)

        main_box.add(button)
        #main_box.add(view)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    async def get_response_from_gemini(self, query):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        response = self.ai.get_response(query, stream=True)

        for chunk in response:
            tts = gTTS(text=chunk.text, lang='en', slow=False)

            # Save the audio file
            tts.save(dir_path + "/photos/tts.mp3")
            # Play the audio file
            aud_path = dir_path + "/photos/tts.mp3"
            os.system(f"afplay -r 1.5 {aud_path}")
    async def uploading_video(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for i in range(10):
            ret, frame = self.cap.read()
            if not ret:
                break
            resize = cv2.resize(frame, (38, 66))
            cv2.imwrite(dir_path+"/photos/newPhoto.png", resize)
            file = File(dir_path+"/photos/newPhoto.png", (str(datetime.now()-self.starting).split(".")[0][2:]))
            self.ai.upload_frame(file)
    async def save_picture(self, widget,**kwargs):
        self.camera.request_permission()
        dir_path = os.path.dirname(os.path.realpath(__file__))


        self.cap = cv2.VideoCapture(0)
        frames_captured = 0
        self.uploading_video()
        while self.cap.isOpened():
            task1 = asyncio.create_task(self.uploading_video())
            task2 = asyncio.create_task(self.get_response_from_gemini())

            await task1
            await task2

            frames_captured += 10

        # while self.cap.isOpened():
        #     ret, frame = self.cap.read()
        #     if not ret:
        #         break
        #     resize = cv2.resize(frame, (38, 66))
        #     cv2.imwrite(dir_path+"/photos/newPhoto.png", resize)
        #     file = File(dir_path+"/photos/newPhoto.png", (str(datetime.now()-self.starting).split(".")[0][2:]))
        #     self.ai.upload_frame(file)
        #     frames_captured += 1
        #     if (frames_captured % 10 == 0):
        #         query = None if frames_captured == 0 else "Did anything change significantly?"
        #         task = asyncio.create_task(self.get_response_from_gemini(query))
                
            #sleep(0.5)
        # d = photo.data
        # im = img.open(BytesIO(d))
        # im.show()

    # def activate_camera(self, widget, **kwargs):
    #     #self.camera.request_permission()
    #     #photo = self.camera.take_photo()
    #     #return photo
    #     pygame.camera.init() 
  
    #     # make the list of all available cameras 
    #     camlist = pygame.camera.list_cameras() 
  
    #     # if camera is detected or not 
    #     if camlist: 
    #         # initializing the cam variable with default camera 
    #         cam = pygame.camera.Camera(camlist[0], (640, 480)) 
    #         # opening the camera 
    #         cam.start() 
    #         # capturing the single image 
    #         image = cam.get_image() 
    #         pygame.display.set_caption('image')
    #         # saving the image 
    #         pygame.image.save(image, "filename.jpg")
  
# if camera is not detected the moving to else part 
                


def main():
    return VisuAIizeApp()

