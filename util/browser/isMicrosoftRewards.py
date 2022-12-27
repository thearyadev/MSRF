import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time


def isMicrosoftRewards(browser: WebDriver) -> bool:
    """
    Checks to see if the current page is the correct Microsoft Rewards page.
    :browser Selenium webdriver
    """
    logger: logging.Logger = logging.getLogger("msrf")  # get logger

    if browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').get_attribute(
            'target') == '_blank':
        browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').click()
        time.sleep(1)
        browser.switch_to.window(window_name=browser.window_handles[0])
        browser.close()
        browser.switch_to.window(window_name=browser.window_handles[0])
        time.sleep(10)
        logger.info("URL is valid.")
        return True
    else:
        logger.warning(f"URL is not valid Redirect to https://account.microsoft.com/rewards")
        return False
