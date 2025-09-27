from app import create_app
from config import Config   # adjust import if Config is defined elsewhere

app = create_app(Config)
