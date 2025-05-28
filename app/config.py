# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
INPUT_SHEET_ID = "19C9mB_2pBM0Qcpc-qGOeDEEvSSaYAW7B4bKi3tTfD1U"
OUTPUT_SHEET_ID = "1u6OtOpUuw5beAE-55hFsABxEsJXWxfyzxzxXFviE7Ck"
KEYWORDS_COLUMN = "keywords"
MAX_PAGES = 10
SERVICE_ACCOUNT_FILE = "credentials/service_account.json"
