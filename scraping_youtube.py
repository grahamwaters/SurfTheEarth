# import build
from googleapiclient.discovery import build
import datetime
import json

# read from secrets.json
with open("secrets.json") as f:
    secrets = json.load(f)
api_key = secrets["youtube_api_key"]
youtube = build("youtube", "v3", developerKey=api_key)

# Search for live streaming videos containing the keyword "webcam" or "Webcam" and the name of a location of some kind like a famous beach or landmark. Use NLTK or TextBlob to detect the entities and locations.

search_response = youtube.search().list(
    part="snippet",
    eventType="live",
    type="video",
    q="webcam",
    maxResults=50,
).execute()

# Print the title of each video.
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        print(search_result["snippet"]["title"])

# Print the video ID of each matching video.
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        print(search_result["id"]["videoId"])

# Save the video ID of each matching video to a list of watchable urls for youtube.
watchable_urls = []
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        watchable_urls.append("https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])

# Save those urls to `./data/watchable_urls.csv` for later use.
with open("data/watchable_urls.csv", "w") as f:
    for url in watchable_urls:
        f.write(url + "\n ")
