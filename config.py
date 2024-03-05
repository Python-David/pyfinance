import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Application settings
APP_TITLE = "PyFinance"

# Date format
DATE_FORMAT = os.environ.get("DATE_FORMAT", "%Y-%m-%d")

# Maximum date
MAX_DATE = os.environ.get("MAX_DATE", "19-12-2014")

# CSV settings
EXPENSE_CSV_PATH = os.environ.get("EXPENSE_CSV_PATH", "expenses.csv")
INVESTMENT_CSV_PATH = os.environ.get("INVESTMENT_CSV_PATH", "investments.csv")
EXPENSE_CSV_HEADERS = ["CATEGORY", "AMOUNT", "DATE", "DESCRIPTION"]
INVESTMENT_CSV_HEADERS = ["TYPE", "AMOUNT", "DATE", "DESCRIPTION"]

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

# Convert DATABASE_URL to individual components if needed
if DATABASE_URL:
    import urllib.parse as urlparse

    url = urlparse.urlparse(DATABASE_URL)
    DATABASE_CONFIG = {
        "user": url.username,
        "password": url.password,
        "database": url.path[1:],
        "host": url.hostname,
        "port": url.port,
    }
else:
    DATABASE_CONFIG = {
        "user": os.environ.get("POSTGRES_USER", "pyfinance_user"),
        "password": os.environ.get("POSTGRES_PASSWORD", "pyfinance_pass"),
        "database": os.environ.get("POSTGRES_DB", "pyfinance_db"),
        "host": "localhost",
        "port": 5431,
    }
