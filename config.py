from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
APP_TITLE = "PyFinance"
DATE_FORMAT = "%Y-%m-%d"
MAX_DATE = 19-12-2014
EXPENSE_CSV_HEADERS = ["CATEGORY", "AMOUNT", "DATE"]
INVESTMENT_CSV_HEADERS = ["TYPE", "AMOUNT", "DATE"]
