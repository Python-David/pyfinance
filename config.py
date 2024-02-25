from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
APP_TITLE = os.getenv("APP_TITLE")
