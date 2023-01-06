import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def waitUntilQuestionRefresh(browser: WebDriver):
    tries = 0
    refreshCount = 0
    while True:
        try:
            _ = browser.find_elements(By.CLASS_NAME, 'rqECredits')[0]  # exception will be thrown
            return True # if no exception
        except Exception as e:
            if tries < 10:
                tries += 1
                time.sleep(0.5)
            else:
                if refreshCount < 5:
                    browser.refresh()
                    refreshCount += 1
                    tries = 0
                    time.sleep(5)
                else:
                    return False
