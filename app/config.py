import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    API_BASE_URL = os.getenv('API_BASE_URL')
    API_KEY = os.getenv('API_KEY')
    API_PREFIX = os.getenv('API_PREFIX', '/api')
    # API_NAMESPACE = os.getenv('API_NAMESPACE', '/sjtu')
