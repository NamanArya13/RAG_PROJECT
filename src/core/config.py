import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
settings = Settings()