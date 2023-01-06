import random
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    browser.find_element(By.ID, "btoption" + str(random.randint(0, 1))).click()
    time.sleep(random.randint(10, 15))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)
