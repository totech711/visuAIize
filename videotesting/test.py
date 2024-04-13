import os
import google.generativeai as genai
     
key = os.environ["API_KEY"]
genai.configure(api_key=key)

file_path = os.path.dirname(os.path.realpath(__file__))

video_path = f"{file_path}/videos/IMG_2946.MOV"

import cv2
import os
import shutil

# Create or cleanup existing extracted image frames directory.
FRAME_EXTRACTION_DIRECTORY = file_path + "/content/frames"
FRAME_PREFIX = "_frame"
def create_frame_output_dir(output_dir):
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  else:
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def extract_frame_from_video(video_file_path):
  print(f"Extracting {video_file_path} at 1 frame per second. This might take a bit...")
  vidcap = cv2.VideoCapture(video_file_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  frame_duration = 1 / fps  # Time interval between frames (in seconds)
  output_file_prefix = os.path.basename(video_file_path).replace('.', '_')
  frame_count = 0
  count = 0
  while vidcap.isOpened():
      success, frame = vidcap.read()
      if not success: # End of video
          break
      if int(count / fps) == frame_count: # Extract a frame every second
          min = frame_count // 60
          sec = frame_count % 60
          time_string = f"{min:02d}:{sec:02d}"
          image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
          output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
          cv2.imwrite(output_filename, frame)
          frame_count += 1
      count += 1
  vidcap.release() # Release the capture object\n",
  print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

extract_frame_from_video(video_path)


class File:
  def __init__(self, file_path: str, display_name: str = None):
    self.file_path = file_path
    if display_name:
      self.display_name = display_name
    self.timestamp = get_timestamp(file_path)

  def set_file_response(self, response):
    self.response = response

def get_timestamp(filename):
  parts = filename.split(FRAME_PREFIX)
  if len(parts) != 2:
      return None  # Indicates the filename might be incorrectly formatted
  return parts[1].split('.')[0]

# Process each frame in the output directory
files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
files = sorted(files)
files_to_upload = []
for file in files:
  files_to_upload.append(
      File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))


# Upload the files to the API
# Only upload a 10 second slice of files to reduce upload time.
# Change full_video to True to upload the whole video.
full_video = True

uploaded_files = []
print(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')

for file in files_to_upload if full_video else files_to_upload[:1]:
  print(file.file_path)
  print(f'Uploading: {file.file_path}...')
  response = genai.upload_file(path=file.file_path)
  file.set_file_response(response)
  uploaded_files.append(file)

print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")

# Create the prompt.
prompt = "Imagine the video given is from your perspective. Describe the scene, including the people in the scene, the objects in the scene, and anything interesting that happens. Make sure to note where objects and people are relative to you, in the last frame."

# Set the model to Gemini 1.5 Pro.
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Make GenerateContent request with the structure described above.
def make_request(prompt, files):
  request = [prompt]
  for file in files:
    request.append(file.timestamp)
    request.append(file.response)
  return request

# Make the LLM request.
request = make_request(prompt, uploaded_files)
response = model.generate_content(request,
                                  request_options={"timeout": 600})
print(response.text)

print(f'Deleting {len(uploaded_files)} images. This might take a bit...')
for file in uploaded_files:
  genai.delete_file(file.response.name)
  print(f'Deleted {file.file_path} at URI {file.response.uri}')
print(f"Completed deleting files!\n\nDeleted: {len(uploaded_files)} files")