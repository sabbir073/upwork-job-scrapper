# app/sheets.py

import gspread
from google.oauth2.service_account import Credentials
from app.config import SERVICE_ACCOUNT_FILE, INPUT_SHEET_ID, OUTPUT_SHEET_ID

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
client = gspread.authorize(creds)


def get_keywords(column_name):
    sheet = client.open_by_key(INPUT_SHEET_ID).sheet1
    values = sheet.col_values(sheet.find(column_name).col)
    return values[1:]  # Skip header


def get_existing_job_ids():
    sheet = client.open_by_key(OUTPUT_SHEET_ID).sheet1
    return set(row[0] for row in sheet.get_all_values()[1:])


def append_job_rows(rows):
    sheet = client.open_by_key(OUTPUT_SHEET_ID).sheet1
    sheet.append_rows(rows)
