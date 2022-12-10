from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver


def getPointCount(browser: WebDriver, BASE_URL: str) -> int:
    browser.get(BASE_URL)
    try:
        return int(browser.find_element(By.XPATH, "//mee-rewards-counter-animation//span").text)
    except:
        return 0
