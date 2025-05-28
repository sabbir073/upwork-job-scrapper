# app/runner.py

from app.scraper import create_browser, scrape_jobs_for_keyword
from app.sheets import get_keywords, get_existing_job_ids, append_job_rows
from app.webhook import send_webhook_response
from app.config import KEYWORDS_COLUMN, MAX_PAGES


def run_scraper():
    keywords = get_keywords(KEYWORDS_COLUMN)
    known_ids = get_existing_job_ids()
    all_new_jobs = []
    processed_keywords = []

    browser = create_browser()

    for keyword in keywords:
        print(f"Scraping keyword: {keyword}")
        jobs, duplicate_hit = scrape_jobs_for_keyword(browser, keyword, known_ids, MAX_PAGES)

        if jobs:
            all_new_jobs.extend(jobs)
            known_ids.update([row[0] for row in jobs])

        processed_keywords.append(keyword)

        if duplicate_hit and keyword == keywords[-1]:
            break

    if all_new_jobs:
        append_job_rows(all_new_jobs)

    browser.quit()

    send_webhook_response("success", processed_keywords, len(all_new_jobs))
