# config.py
from dotenv import load_dotenv
import os

load_dotenv()

assistant_id = os.getenv("ASSISTANT_ID")
client_api_key = os.getenv("CLIENT_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")
