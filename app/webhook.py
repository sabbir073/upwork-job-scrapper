# app/webhook.py

import requests
from app.config import WEBHOOK_URL

def send_webhook_response(status, keywords, new_jobs):
    if not WEBHOOK_URL:
        print("No webhook URL configured.")
        return

    payload = {
        "status": status,
        "keywords_processed": keywords,
        "new_jobs": new_jobs,
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        print("Webhook sent, status:", response.status_code)
    except Exception as e:
        print("Failed to send webhook:", str(e))
