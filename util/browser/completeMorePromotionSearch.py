import logging

from selenium.webdriver.chrome.webdriver import WebDriver

from selenium.webdriver.common.by import By
import time
import random
from util import deprecated


def complete_more_promotion_search(*, browser: WebDriver, cardNumber: int):
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    logger.info("Completing promotion search")
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)
