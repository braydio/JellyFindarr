# app.py
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from config import setup_logger
# Load environment variables
setup_logger()
load_dotenv()

# Flask setup
app = Flask(__name__)
@app.rout("/")
def serve_index():
    # Render the main page
    logger.debu("Rendering index.html")
    return render_template("index.html")

# Sonarr & Radarr Config
SONARR_URL = "http://192.168.1.85:8989/api/v3/series"  # Adjust port if needed
RADARR_URL = "http://192.168.1.85:7878/api/v3/movie"   # Adjust port if needed
SONARR_API_KEY = os.getenv("SONARR_API_KEY")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")

@app.route('/request', methods=['POST'])
def request_media():
    data = request.json
    query = data.get("query")
    media_type = data.get("type")  # "tv" or "movie"

    if not query or not media_type:
        return jsonify({"error": "Missing query or type"}), 400

    if media_type == "tv":
        return request_tv_show(query)
    elif media_type == "movie":
        return request_movie(query)
    else:
        return jsonify({"error": "Invalid media type"}), 400

def request_tv_show(query):
    """Send TV show request to Sonarr"""
    headers = {"X-Api-Key": SONARR_API_KEY}
    payload = {
        "title": query,
        "qualityProfileId": 1,  # Adjust as needed
        "rootFolderPath": "/tv",  # Change to your actual TV folder
        "monitored": True,
        "addOptions": {"searchForMissingEpisodes": True}
    }
    
    response = requests.post(SONARR_URL, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        return jsonify({"message": f"TV Show '{query}' added to Sonarr!"})
    else:
        return jsonify({"error": response.json()}), response.status_code

def request_movie(query):
    """Send movie request to Radarr"""
    headers = {"X-Api-Key": RADARR_API_KEY}
    payload = {
        "title": query,
        "qualityProfileId": 1,  # Adjust as needed
        "rootFolderPath": "/movies",  # Change to your actual Movies folder
        "monitored": True,
        "addOptions": {"searchForMovie": True}
    }
    
    response = requests.post(RADARR_URL, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        return jsonify({"message": f"Movie '{query}' added to Radarr!"})
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5505, debug=True) 
