from classes import *
import os
key = os.environ["API_KEY"]
key2 = os.environ["API_KEY2"]
#photo input simulation
file_path = os.path.dirname(os.path.realpath(__file__))
dir_path = file_path + "/content/vid0/"
ai = VideoGemini(api_keys=[key, key2], verbose = True, delete = False)
for filename in os.listdir(dir_path):
    file_os = os.path.join(dir_path, filename)
    timestamp = filename.split("_frame")[1].split(".")[0][:-3]
    print(timestamp)
    # checking if it is a file
    if os.path.isfile(file_os):
        file = File(file_os, timestamp)
        ai.upload_frame(file)

resp = ai.get_response()
print(resp)
dir_path = file_path + "/content/vid1/"
for filename in os.listdir(dir_path):
    file_os = os.path.join(dir_path, filename)
    timestamp = filename.split("_frame")[1].split(".")[0][:-3]
    print(timestamp)
    # checking if it is a file
    if os.path.isfile(file_os):
        file = File(file_os, timestamp)
        ai.upload_frame(file)

resp = ai.get_response("Did anything significant change from the last scene? If so, give me the description.")
print(resp)

dir_path = file_path + "/content/vid2/"
for filename in os.listdir(dir_path):
    file_os = os.path.join(dir_path, filename)
    timestamp = filename.split("_frame")[1].split(".")[0][:-3]
    print(timestamp)
    # checking if it is a file
    if os.path.isfile(file_os):
        file = File(file_os, timestamp)
        ai.upload_frame(file)

resp = ai.get_response("Did anything significant change from the last scene? If so, give me the description.")
print(resp)

dir_path = file_path + "/content/vid3/"
for filename in os.listdir(dir_path):
    file_os = os.path.join(dir_path, filename)
    timestamp = filename.split("_frame")[1].split(".")[0][:-3]
    print(timestamp)
    # checking if it is a file
    if os.path.isfile(file_os):
        file = File(file_os, timestamp)
        ai.upload_frame(file)

resp = ai.get_response("Did anything significant change from the last scene? If so, give me the description.")
print(resp)