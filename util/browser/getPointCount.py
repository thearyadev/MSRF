import logging

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import re

import util


def getPointCount(browser: WebDriver) -> int:
    """
    Navigates to bing.com as an authenticated user. Gets the point count and returns it.
    Defaults to 0 if the function fails.
    :browser Selenium web driver
    """
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    data = util.get_dashboard_data(browser)
    try:
        return data.get("userStatus").get("availablePoints") if data.get("userStatus").get("availablePoints") else 0
    except AttributeError as e:
        logger.critical(f"Point count not available. Likely dashboard data has changed. {e}")
    except Exception as e:
        logger.critical(f"Unexpected exception {e}")

    return 0
