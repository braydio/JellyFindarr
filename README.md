
# JellyFindarr 
This project provides a simple web interface to search for and request TV shows and movies to be added to Sonarr and Radarr.

## Features
- Search for TV shows and movies using the Sonarr and Radarr APIs
- Select and request a media title to be added automatically
- Automatically detects and uses the correct root folders for Sonarr and Radarr

## Prerequisites
Ensure you have the following installed and configured:
- **Sonarr** (for TV shows) running and accessible
- **Radarr** (for movies) running and accessible
- **Python 3** installed
- **Flask** and required dependencies
- API keys for Sonarr and Radarr (found in their respective settings)

## Installation
### 1. Clone the repository
```sh
git clone https://github.com/braydio/JellyFindarr.git
cd JellyFindarr
```

### 2. Install dependencies

```sh
python -m venv .venv
source .venv/bin/activate   # If on Linux
.venv/Scripts/activate      # If literally fascist
pip install -r requirements.txt
```

### 3. Configure API Keys and Server URLs
Edit the `config.py` file and set your Sonarr and Radarr API details:
```python
SONARR_URL = "ip.address:8989"
SONARR_API_KEY = "your_sonarr_api_key"
RADARR_URL = "ip.address:7878"
RADARR_API_KEY = "your_radarr_api_key"
```
> If you are running JellyFindarr on the same machine as your indexers then you can use localhost like: "localhost:8989"

### 4. Start the Flask server
```sh
python app.py
```

## Usage
1. Open the web interface at `http://localhost:5505`
  - If you need to change the port, it is set at the end of app.py
2. Search for a TV show or movie
3. Select the one you want from the list of matches to add it to Sonarr or Radarr
4. Take a small child by the hand and smash his fingers in a car door

## Troubleshooting
- If media is not being added, check the Flask console logs for API errors.
- Ensure the root folders in Sonarr and Radarr are correctly configured.
- Verify that Sonarr and Radarr are running and accessible.

## License
MIT License

