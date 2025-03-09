
import json
from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
from config import SONARR_URL, SONARR_API_KEY, RADARR_URL, RADARR_API_KEY

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route("/")
def serve_index():
    return render_template("index.html")


@app.route('/search', methods=['GET'])
def search_media():
    """Searches for a movie/TV show and returns a list of results."""
    query = request.args.get("query")
    media_type = request.args.get("type")

    if not query or not media_type:
        return jsonify({"error": "Missing query or type"}), 400

    if media_type == "tv":
        url = f"{SONARR_URL}/api/v3/series/lookup?term={query}"
        headers = {"X-Api-Key": SONARR_API_KEY}
    else:
        url = f"{RADARR_URL}/api/v3/movie/lookup?term={query}"
        headers = {"X-Api-Key": RADARR_API_KEY}

    response = requests.get(url, headers=headers)
    print("Search Response:", response.status_code, response.text)  # Log response

    if response.status_code != 200 or not response.json():
        return jsonify([])

    return jsonify([
        {
            "id": item.get("tvdbId") if media_type == "tv" else item.get("tmdbId"),
            "title": item.get("title"),
            "year": item.get("year", "N/A")
        }
        for item in response.json()
    ])


@app.route('/request', methods=['POST'])
def request_media():
    """Adds the selected movie/TV show."""
    data = request.json
    media_id = data.get("id")
    title = data.get("title")
    media_type = data.get("type")

    if not media_id or not title or not media_type:
        return jsonify({"error": "Missing ID, title, or type"}), 400

    if media_type == "tv":
        return request_tv_show(media_id, title)
    else:
        return request_movie(media_id, title)


### **✅ Fetch Correct Sonarr Root Folder**
def get_sonarr_root_folder():
    """Fetches the first available root folder from Sonarr."""
    url = f"{SONARR_URL}/api/v3/rootfolder"
    headers = {"X-Api-Key": SONARR_API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()[0]["path"]  # Use the first available root folder
    return None


### **✅ Improved Sonarr TV Show Request**
def request_tv_show(tvdb_id, title):
    """Send TV show request to Sonarr"""
    root_folder = get_sonarr_root_folder()
    if not root_folder:
        return jsonify({"error": "No valid root folder found in Sonarr"}), 500

    url = f"{SONARR_URL}/api/v3/series"
    payload = {
        "tvdbId": tvdb_id,
        "title": title,
        "titleSlug": title.lower().replace(" ", "-"),
        "qualityProfileId": 1,
        "rootFolderPath": root_folder,
        "monitored": True,
        "addOptions": {"searchForMissingEpisodes": True}
    }
    headers = {"X-Api-Key": SONARR_API_KEY}

    print("Sending Request to Sonarr:", url)
    print("Payload:", json.dumps(payload, indent=4))  # Log the payload

    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.status_code, response.text)  # Log the response

    if response.status_code in [200, 201]:
        return jsonify({"message": f"TV Show '{title}' added to Sonarr!"})
    else:
        return jsonify({"error": response.json()}), response.status_code


### **✅ Fetch Correct Radarr Root Folder**
def get_radarr_root_folder():
    """Fetches the first available root folder from Radarr"""
    url = f"{RADARR_URL}/api/v3/rootfolder"
    headers = {"X-Api-Key": RADARR_API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()[0]["path"]  # Use the first available root folder
    return None


### **✅ Improved Radarr Movie Request**
def request_movie(tmdb_id, title, year=None):
    """Send movie request to Radarr"""
    root_folder = get_radarr_root_folder()
    if not root_folder:
        return jsonify({"error": "No valid root folder found in Radarr"}), 500

    url = f"{RADARR_URL}/api/v3/movie"
    
    # Build the payload, but exclude "year" if it's None
    payload = {
        "tmdbId": tmdb_id,
        "title": title,
        "qualityProfileId": 1,
        "rootFolderPath": root_folder,
        "monitored": True,
        "addOptions": {"searchForMovie": True}
    }

    if year:  # Only add the year if it's valid
        payload["year"] = int(year)  # Ensure year is an integer

    headers = {"X-Api-Key": RADARR_API_KEY}

    print("Sending Request to Radarr:", url)
    print("Payload:", json.dumps(payload, indent=4))  # Debugging

    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.status_code, response.text)  # Debugging

    if response.status_code in [200, 201]:
        return jsonify({"message": f"Movie '{title}' added to Radarr!"})
    else:
        return jsonify({"error": response.json()}), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5505, debug=True)

