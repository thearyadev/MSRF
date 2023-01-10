import time
import typing

import selenium.common.exceptions
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import custom_logging
import util

if typing.TYPE_CHECKING:
    pass


def authenticate_microsoft_account(*, browser: WebDriver, account: util.MicrosoftAccount) -> bool:
    """
    Logs into Microsoft Rewards (and bing) in the current browser instance for the given account.
    :browser Selenium webdriver
    :account MicrosoftAccount object
    """
    from util import ErrorReport, ErrorReporter
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)

    # Access to bing.com
    logger.info("Navigating to https://login.live.com/")
    browser.get('https://login.live.com/')

    # Wait for the page to load
    try:
        util.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    except selenium.common.exceptions.TimeoutException:
        logger.warning("Element loginHeader has not loaded.")

    # Enter email
    logger.info("Writing email...")
    try:
        browser.find_element(By.NAME, "loginfmt").send_keys(account.email)
    except selenium.common.exceptions.NoSuchElementException:
        logger.warning("Login text field does not exist. loginfmt")
    except selenium.common.exceptions.ElementNotInteractableException:
        logger.warning("Login text field is not intractable. loginfmt")
    except Exception as e:
        logger.error(f"Error uncaught. Likely unable to log in.")

    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
    except selenium.common.exceptions.NoSuchElementException:
        logger.warning("Login next button not found. Likely unable to log in idSIButton9")
    except selenium.common.exceptions.ElementNotInteractableException:
        logger.warning("Login next button not intractable. idSIButton9")
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Error uncaught. Likely unable to log in. "
                        f"Error report has been generated: {errorReport.file_path}")

    # Wait 2 seconds
    time.sleep(2)
    # Wait complete loading of the password field.
    try:
        util.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    except selenium.common.exceptions.TimeoutException:
        logger.warning("loginHeader is not visible. Password field may be inaccessible. Attempting login anyway.")

    # Enter password
    # browser.find_element(By.ID, "i0118").send_keys(pwd)
    # TODO
    # determine which password entry method works.
    logger.info("Writing password...")
    browser.execute_script("document.getElementById('i0118').value = '" + account.password + "';")

    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
    except selenium.common.exceptions.NoSuchElementException:
        logger.warning("Password next button does not exist.")
    except selenium.common.exceptions.ElementNotInteractableException:
        logger.warning("Password next button is not interactable")
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Error uncaught. Likely unable to log in. "
                        f"Error report has been generated: {errorReport.file_path}")
    # Wait 5 seconds
    time.sleep(5)

    # Click Security Check
    logger.info("Passing security checks...")
    try:
        browser.find_element(By.ID, 'iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        logger.warning(f"iLandingViewAction element is unreachable.")
    try:
        browser.find_element(By.ID, 'iNext').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        logger.warning(f"iNext element is unreachable.")
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Caught unknown error during security check pass. Login state uncertain "
                        f"Error report has been generated: {errorReport.file_path}")

    # Wait complete loading
    try:
        util.waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)  # wait 10 sec for the element to load
    except TimeoutException as e:
        logger.warning("Element KmsiCheckboxField not detected. Timeout or element does not exist.")

    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        logger.warning(f"idSIButton9 element is unreachable.. Login state uncertain")
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Caught unknown error during security check pass. Login state uncertain."
                        f"Error report has been generated: {errorReport.file_path}")

    # Check Login in Bing.
    logger.info("Validating Bing login state...")
    try:
        return util.verify_bing_login(browser)
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Uncaught error in validating bing login. "
                        f"Error report has been generated: {errorReport.file_path}")
