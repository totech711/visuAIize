from moviepy.editor import VideoFileClip
from time import sleep
import os
file_path = os.path.dirname(os.path.realpath(__file__))
dir_path = file_path + "../capture/testvid.MOV"
full_video = "full.mp4"
current_duration = VideoFileClip(dir_path).duration
divide_into_count = 150
single_duration = current_duration/divide_into_count
current_video = f"{current_duration}.mp4"

while current_duration > single_duration:
    clip = VideoFileClip(dir_path).subclip(current_duration-single_duration, current_duration)
    current_duration -= single_duration
    current_video = f"{current_duration}.mp4"
    clip.to_videofile(current_video, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

    print("-----------------###-----------------")