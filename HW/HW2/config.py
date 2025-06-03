import os
from dotenv import load_dotenv


load_dotenv()  


API_TOKEN = os.getenv("API_TOKEN")
COMMON_URL = os.getenv("COMMON_URL")

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

BASE_URL = f"{COMMON_URL}{os.getenv('BASE_URL')}"
GENRE_URL = f"{COMMON_URL}{os.getenv('GENRE_URL')}"
