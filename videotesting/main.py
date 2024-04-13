"""from classes import *
import os
import asyncio
key = os.environ["API_KEY"]
#key2 = os.environ["API_KEY2"]
#photo input simulation
file_path = os.path.dirname(os.path.realpath(__file__))
dir_path = file_path + "/capture/test/"
ai = VideoGemini(api_keys=[key], verbose = True, delete = False)
for filename in os.listdir(dir_path):
    file_os = os.path.join(dir_path, filename)
    timestamp = filename.split("_frame")[1].split(".")[0][:-3]
    print(timestamp)
    # checking if it is a file
    if os.path.isfile(file_os):
        file = File(file_os, timestamp)
        ai.upload_frame(file)
async def runthestuff():
    task = asyncio.create_task(ai.get_response_async())
    print("hahahahaha")
    await task
asyncio.run(runthestuff())"""

from time import sleep
from datetime import datetime

starting = datetime.now()
sleep(1)
print(str(datetime.now() - starting).split(".")[0][2:])
