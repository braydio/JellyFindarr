import logging
import os 
from dotenv import load_dotenv
from pathlib import Path

# Set up logging
def setup_logger():
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # File handler
        log_file = "index.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler) 
        logger.addHandler(console_handler) 

        return logger

logger = setup_logger()

# Initialize environment
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = "index.html"

# Sonarr & Radarr Config
SONARR_URL = os.getenv("SONARR_WEB_URL", "localhost:8989")
RADARR_URL = os.getenv("RADARR_WEB_URL", "localhost:7878")
LIDARR_URL = os.getenv("LIDARR_WEB_URL", "localhost:7878")

SONARR_API_KEY = os.getenv("SONARR_API_KEY")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
LIDARR_API_KEY = os.getenv("LIDARR_API_KEY")

logger.debug(f"IP Addies: {SONARR_URL}  {RADARR_URL}  {LIDARR_URL}")
