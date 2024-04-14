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

        #my_image = toga.Image("filename.png")
        #view = toga.ImageView(my_image)

        main_box.add(button)
        #main_box.add(view)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    async def save_picture(self, widget,**kwargs):
        self.camera.request_permission()
        dir_path = os.path.dirname(os.path.realpath(__file__))


        cap = cv2.VideoCapture(0)
        frames_captured = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            sleep(0.5)
            cv2.imwrite(dir_path+"/photos/newPhoto.png", frame)
            file = File(dir_path+"/photos/newPhoto.png", (str(datetime.now()-self.starting).split(".")[0][2:]))
            self.ai.upload_frame(file)
            frames_captured += 1
            if (frames_captured % 10 == 0):
                query = None if frames_captured == 0 else "Did anything change significantly?"
                response = await self.ai.async_get_response(query)
                print(response)
                tts = gTTS(text=response, lang='en', slow=False)

                # Save the audio file
                tts.save(dir_path + "/photos/tts.mp3")
                
                # Play the audio file
                aud_path = dir_path + "/photos/tts.mp3"
                os.system(f"afplay {aud_path}")
                
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

