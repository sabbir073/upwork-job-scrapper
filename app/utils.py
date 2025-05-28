import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_delay(min_sec=2, max_sec=4):
    time.sleep(random.uniform(min_sec, max_sec))

def wait_for_element(browser, by, value, timeout=15):
    return WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def scroll_to_bottom(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
