from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TTS_API_URL = os.getenv('TTS_API_URL')
    IMAGE_SERVER_ADDRESS = os.getenv('IMAGE_SERVER_ADDRESS') 