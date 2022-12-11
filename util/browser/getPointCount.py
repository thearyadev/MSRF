from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time


def getPointCount(browser: WebDriver, BASE_URL: str) -> int:
    browser.get(BASE_URL)
    try:
        time.sleep(3)
        return int(browser.find_elements(By.CLASS_NAME, "pointsValue")[0].text)
    except:
        return 0
