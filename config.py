import logging
import os 
from dotenv import load_dotenv
from pathlib import Path

# Initialize environment
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = "index.html"

# Sonarr & Radarr Config
SONARR_URL = "http://192.168.1.85:8989"  # Adjust port if needed
RADARR_URL = "http://192.168.1.85:7878"   # Adjust port if needed
SONARR_API_KEY = os.getenv("SONARR_API_KEY")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")

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
