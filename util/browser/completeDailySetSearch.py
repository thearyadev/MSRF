import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import random


def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card['
                         + str(cardNumber)
                         + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)
