import logging
import random
import time

from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoAlertPresentException,
                                        NoSuchElementException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import custom_logging
import util


def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)

    browser.get('https://bing.com')
    time.sleep(2)
    searchbar = browser.find_element(By.ID, 'sb_form_q')
    searchbar.send_keys(word)
    searchbar.submit()
    time.sleep(random.randint(10, 15))
    points = 0
    try:
        if not isMobile:
            points = int(browser.find_element(By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try:
                browser.find_element(By.ID, 'mHamburger').click()
            except UnexpectedAlertPresentException:
                try:
                    browser.switch_to.alert.accept()
                    time.sleep(1)
                    browser.find_element(By.ID, 'mHamburger').click()
                except NoAlertPresentException:
                    pass
            time.sleep(1)
            points = int(browser.find_element(By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except Exception as e:
        logger.critical(f"Unknown error trying to complete single bing search. {e}")
    return points
