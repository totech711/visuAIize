# VisuAIizer 
VisuAIizer contextualizes the world around you. For blind and visually impaired people, VisuAIizer offers real time video analysis utilizing the recent Gemini 1.5 model. By placing a phone in your shirt pocket the app will record your day and describe your surroundings in real time.

# How it Works

We utilize OpenCV to capture images (frames) of your day, which are uploaded immediately as they are captured to Gemini. Once enough frames are uploaded (usually 5 - 10 seconds worth of video), a Gemini 1.5 API call is made in parallel to frame capture. This reduces latency with Gemini to offer real time analysis. We also prompt engineered to reduce output tokens from Gemini, further reducing latency. 

#Devpost
[https://devpost.com/software/visuaiize](url)
