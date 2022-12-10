import json
import util
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def getDashboardData(browser: WebDriver) -> dict:
    dashboard = util.findBetween(
        browser.find_element(By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
    dashboard = json.loads(dashboard)
    return dashboard
