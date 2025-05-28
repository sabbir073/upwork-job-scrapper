# api.py

from fastapi import FastAPI
from app.runner import run_scraper
import traceback

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Upwork scraper is running."}

@app.post("/start")
def start_scraping():
    try:
        run_scraper()
        return {"status": "Scraping started and finished successfully."}
    except Exception as e:
        print("🔥 ERROR during scraping:")
        traceback.print_exc()
        return {"status": "Error during scraping", "error": str(e)}
