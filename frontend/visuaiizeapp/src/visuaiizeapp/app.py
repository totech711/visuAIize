"""
Build the world around you for you
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga import Image, ImageView, Canvas
# import pygame
# import pygame.camera
import os
import cv2
from time import sleep
from .geminidriver import *


from datetime import datetime
import threading
from gtts import gTTS
import sys




class VisuAIizeApp(toga.App):
   main_box = toga.Box()
   def startup(self):
       dir_path = os.path.dirname(os.path.realpath(__file__))
       with open(dir_path+"/resources/API_KEY.txt","r") as f:
           api_keys = f.read().split("\n")
       key1 = os.environ["API_KEY1"]
       key2 = os.environ["API_KEY2"]
       self.ai = VideoGemini(api_keys=api_keys, verbose=True, delete=False)
       main_box = toga.Box(style=Pack(direction=COLUMN))
       my_image = toga.Image(dir_path+"/resources/logo.png")
       main_box.add(
         toga.ImageView(
             my_image,style=Pack(alignment = 'center', height=100)
         )
       )
       button = toga.Button(
           "START MY DAY",
           on_press=self.save_picture,
           style=Pack(padding=5, background_color=("#8a4cfc"), alignment = 'center', height=200)
       )
       end_button = toga.Button(
           "END MY DAY",
           on_press=self.end_day,
           style=Pack(padding=5, background_color=("#8a4cfc"), direction=COLUMN, alignment = 'center', height=200)
       )


       self.starting = datetime.now()
       self.cap = None


       #my_image = toga.Image("filename.png")
       #view = toga.ImageView(my_image)


       main_box.add(button)
       #main_box.add(view)
       main_box.add(end_button)

       self.main_window = toga.MainWindow(title=self.formal_name)
       self.main_window.content = main_box
       self.main_window.show()
   def get_response_from_gemini(self, query):
       print("arrived gemini")
       dir_path = os.path.dirname(os.path.realpath(__file__))
       response = self.ai.get_response(query)


       tts = gTTS(text=response.text.replace("<None>", ""), lang='en', slow=False)


       # Save the audio file
       tts.save(dir_path + "/photos/tts.mp3")
       # Play the audio file
       aud_path = dir_path + "/photos/tts.mp3"
       os.system(f"afplay -r 1.5 {aud_path}")
   def uploading_video(self):
       print("arrived upload")
       dir_path = os.path.dirname(os.path.realpath(__file__))
       for i in range(10):
           ret, frame = self.cap.read()
           if not ret:
               break
           resize = cv2.resize(frame, (320, 320))
           cv2.imwrite(dir_path+"/photos/newPhoto.png", resize)
           file = File(dir_path+"/photos/newPhoto.png", (str(datetime.now()-self.starting).split(".")[0][2:]))
           self.ai.upload_frame(file)
   def end_day(self, widget, **kwargs):
       sys.exit()
   async def save_picture(self, widget,**kwargs):
       self.camera.request_permission()
       dir_path = os.path.dirname(os.path.realpath(__file__))




       self.cap = cv2.VideoCapture(0)
       frames_captured = 0
      
       while self.cap.isOpened():
           if frames_captured<=15:
               print("before first upload")
               self.uploading_video()
               print("after first upload")


           task1 = threading.Thread(target=self.uploading_video, daemon=True)
           task2 = threading.Thread(target=self.get_response_from_gemini, args=(None, ), daemon=True)
           task1.start()
           task2.start()
           task1.join()
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





