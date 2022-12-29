import json
import logging

import util
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from util import deprecated
from ..models.dashboard_data import DashboardData


@deprecated
def getDashboardData(browser: WebDriver) -> dict:
    dashboard = util.findBetween(
        browser.find_element(By.XPATH, '/html/body')
        .get_attribute('innerHTML'),
        "var dashboard = ",
        ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
    dashboard = json.loads(dashboard)
    return dashboard


@deprecated
def get_dashboard_data(browser: WebDriver) -> dict | None:
    """
    Returns the data from the dashboard
    """
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    logger.info("loading dashboard data")
    try:
        dashboard = util.findBetween(
            browser.find_element(By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ",
            ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
        dashboard = json.loads(dashboard)
    except Exception as e:
        logger.critical(f"Unable to load dashboard data. {e}")
        return None
    return dashboard


def load_dashboard_data(browser: WebDriver) -> DashboardData:
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    logger.info("loading dashboard data")
    try:
        return util.DashboardData(**browser.execute_script("return dashboard"))
    except Exception as e:
        # Since this is breaking, it may be ideal to exit the thread with sys.exit(). tbd.
        logger.critical(f"Unable to load dashboard data. {e}")
