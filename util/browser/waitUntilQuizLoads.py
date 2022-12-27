import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def waitUntilQuizLoads(browser: WebDriver):
    """
    Trys to wait for the quiz to load
    :browser Selenium webdriver
    """

    tries = 0
    refreshCount = 0
    while True:
        try:
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]')
            return True
        except Exception:
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
