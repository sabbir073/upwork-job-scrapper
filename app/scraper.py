import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from undetected_chromedriver import Chrome, ChromeOptions
from app.constants import SEARCH_URL_TEMPLATE
from app.utils import random_delay
from urllib.parse import quote

def create_browser():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    )

    browser = Chrome(options=options)

    # Extra stealth: mask webdriver
    browser.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """
        },
    )
    return browser


def wait_for_element(browser, by, value, timeout=20):
    try:
        WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, value)))
        return True
    except TimeoutException:
        return False


def scrape_jobs_for_keyword(browser, keyword, known_ids, max_pages):
    scraped_jobs = []
    duplicate_hit = False
    encoded_keyword = quote(keyword)

    print(f"\n🔍 Scraping keyword: '{keyword}'")

    for page in range(1, max_pages + 1):
        url = f"{SEARCH_URL_TEMPLATE}?q={encoded_keyword}&page={page}&per_page=50"
        print(f"🌐 Visiting: {url}")

        browser.get(url)
        random_delay(3, 6)

        screenshot_path = f"screenshot_{keyword.replace(' ', '_')}_page_{page}.png"
        browser.save_screenshot(screenshot_path)

        found = wait_for_element(browser, By.CSS_SELECTOR, '[data-test="JobsList"]', timeout=25)

        if not found:
            print("⚠️  JobsList not found — skipping page.")
            continue

        job_cards = browser.find_elements(By.CSS_SELECTOR, 'article[data-test="JobTile"]')

        print(f"📦 Found {len(job_cards)} job cards on this page.")

        for idx, job in enumerate(job_cards, 1):
            try:
                job_id = job.get_attribute("data-ev-job-uid")
                if job_id in known_ids:
                    print(f"⏹️  Duplicate job ID {job_id} found — stopping.")
                    duplicate_hit = True
                    return scraped_jobs, duplicate_hit

                title_elem = job.find_element(By.CSS_SELECTOR, '[data-test*="job-tile-title-link"]')
                job_title = title_elem.text.strip()
                job_url = "https://www.upwork.com" + title_elem.get_attribute("href")

                posted_elem = job.find_element(By.CSS_SELECTOR, '[data-test="job-pubilshed-date"] span:last-child')
                posted_ago = posted_elem.text.strip()

                # Calculate actual post time
                now = datetime.now()  # Local time
                if "minute" in posted_ago:
                    minutes = int(posted_ago.split()[0])
                    post_time = now - timedelta(minutes=minutes)
                elif "hour" in posted_ago:
                    hours = int(posted_ago.split()[0])
                    post_time = now - timedelta(hours=hours)
                else:
                    post_time = now

                job_date = post_time.strftime("%d %B %Y")
                job_time = post_time.strftime("%I:%M %p")

                print(f"📝 Scraping job {idx}: {job_title} [{job_id}]")

                # Simulate visit to job URL (tab simulation will be added later)
                # browser.execute_script("window.open('');")
                # browser.switch_to.window(browser.window_handles[1])
                # browser.get(job_url)
                # ... scrape details ...
                # browser.close()
                # browser.switch_to.window(browser.window_handles[0])

                scraped_jobs.append([
                    job_id,
                    job_date,
                    job_time,
                    job_url,
                    job_title
                ])
            except Exception as e:
                print(f"❌ Error scraping job {idx}: {e}")
                continue

        random_delay(2, 5)

    return scraped_jobs, duplicate_hit
