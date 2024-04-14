from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import cv2
import os

def index(request):
    cap = cv2.VideoCapture(0)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resize = cv2.resize(frame, (320, 320))
        cv2.imwrite(dir_path+"/photos/newPhoto.png", resize)
    return HttpResponse("")