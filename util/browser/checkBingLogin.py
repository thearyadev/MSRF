import time

import selenium.common.exceptions
from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util
from selenium.webdriver.common.by import By
import logging
from util import deprecated


def verify_bing_login(browser: WebDriver) -> bool:
    """
    Uses the bing login homepage to check if the user is logged in.
    This will check the id_n span tag. This tag will contain text if the user is logged in.
    If there is no text (or element does not exist), the user is not logged in.

    :browser Selenium webdriver.
    """
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    # Access Bing.com
    browser.get(
        "https://www.bing.com/fd/auth/signin?action=interactive&provider=windows_live_id&return_url=https%3a%2f%2fwww"
        ".bing.com%2f%3ftoWww%3d1%26redig%3d0A10E5FC496E4B2CB8EFC9C629932938%26wlexpsignin%3d1&src=EXPLICIT&sig"
        "=1555A6A1CA736D690B78B42BCBD96C3E"
    )
    # Wait 8 seconds

    try:
        logger.info("Waiting for browser to load login evidence")
        util.waitUntilVisible(browser, By.ID, "id_n", 8)
    except selenium.common.exceptions.TimeoutException:
        logger.warning("Timeout exception: element may not be loaded.")

    # Check login

    try:
        authenticated_user_title = browser.find_element(By.ID, "id_n")
    except selenium.common.exceptions.NoSuchElementException:
        logger.error("id_n element does not exist.")
        return False  # cant find element. Login failed.
    else:
        # the id_n element will have the users name. This element does not have text if the user is not logged in.
        if authenticated_user_title.text:
            return True  # success
    return False  # guard. Login failed


if __name__ == '__main__':
    config = util.load_config("../../configuration.yaml")
    b = util.init_browser(headless=False, agent=config.pc_user_agent)
