from selenium.webdriver.chrome.webdriver import WebDriver
import util
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException


def login(browser: WebDriver, email: str, pwd: str, logger: util.ConsoleLogger, isMobile: bool = False):
    # Access to bing.com
    browser.get('https://login.live.com/')
    # Wait complete loading
    util.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter email
    logger.log("Writing email...")
    browser.find_element(By.NAME, "loginfmt").send_keys(email)
    # Click next
    browser.find_element(By.ID, 'idSIButton9').click()
    # Wait 2 seconds
    time.sleep(2)
    # Wait complete loading
    util.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter password
    # browser.find_element(By.ID, "i0118").send_keys(pwd)
    browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
    logger.log("Writing password...")
    # Click next
    browser.find_element(By.ID, 'idSIButton9').click()
    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    logger.log("Passing security checks...")
    try:
        browser.find_element(By.ID, 'iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    try:
        browser.find_element(By.ID, 'iNext').click()
    except:
        pass
    # Wait complete loading
    try:
        util.waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)
    except (TimeoutException) as e:
        pass
    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    # Check Login
    logger.log("Validating Bing login state...")
    util.checkBingLogin(browser, isMobile=isMobile, logger=logger)
