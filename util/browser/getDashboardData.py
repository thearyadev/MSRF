import json
import logging

import util
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from util import deprecated


@deprecated
def getDashboardData(browser: WebDriver) -> dict:
    dashboard = util.findBetween(
        browser.find_element(By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ",
        ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
    dashboard = json.loads(dashboard)
    return dashboard


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


if __name__ == '__main__':
    config = util.load_config("../../configuration.yaml")
    b = util.init_browser(headless=False, agent=config.pc_user_agent)
