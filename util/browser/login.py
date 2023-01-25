import time
import typing

import selenium.common.exceptions
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import JavascriptException

import custom_logging
import util

if typing.TYPE_CHECKING:
    pass


def authenticate_microsoft_account_legacy(*, browser: WebDriver, account: util.MicrosoftAccount) -> bool:
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
    time.sleep(2)
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


def authenticate_microsoft_account(*, browser: WebDriver, account: util.MicrosoftAccount) -> bool:
    from util import ErrorReport, ErrorReporter
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    logger.info("Navigating to https://login.live.com/")
    browser.get('https://login.live.com/')

    # Wait for the page to load
    try:
        util.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    except selenium.common.exceptions.TimeoutException:
        logger.warning("Element loginHeader has not loaded.")

    try:
        browser.find_element(By.NAME, "loginfmt").send_keys(account.email)
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Uncaught error authentication during Email phase."
                        f"Error report has been generated: {errorReport.file_path}")

    time.sleep(2)

    try:
        browser.find_element(By.ID, 'idSIButton9').click()
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Error uncaught while trying to click the next button after entering email."
                        f"Error report has been generated: {errorReport.file_path}")

    time.sleep(2)

    try:
        passwordField = browser.find_element(By.NAME, "passwd")
        passwordField.send_keys(account.password)
        time.sleep(1)
        passwordField.send_keys(Keys.ENTER)  # submit login
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.error(f"Error uncaught while trying to enter and submit password."
                     f"Error report has been generated: {errorReport.file_path}")
    browser.get("https://rewards.bing.com")
    time.sleep(2)
    logger.info("Verifying login is successful")
    try:
        browser.execute_script("return dashboard")
        logger.info("https://rewards.bing.com is authenticated.")
    except JavascriptException:
        logger.critical("Login failed. https://rewards.bing.com is not authenticated.")
        return False

    browser.get(
        "https://www.bing.com/fd/auth/signin?action=interactive&provider=windows_live_id&return_url=https%3a%2f%2fwww"
        ".bing.com%2f%3ftoWww%3d1%26redig%3d0A10E5FC496E4B2CB8EFC9C629932938%26wlexpsignin%3d1&src=EXPLICIT&sig"
        "=1555A6A1CA736D690B78B42BCBD96C3E"
    )

    try:
        util.waitUntilVisible(browser, By.ID, "id_n", 8)
    except selenium.common.exceptions.TimeoutException:
        logger.warning("Timeout exception: element may not be loaded.")

    # Check login

    try:
        authenticated_user_title = browser.find_element(By.ID, "id_n").text
        if authenticated_user_title and authenticated_user_title != account.email:
            logger.warning("Login uncertain. Bing authenticated user is not the same as the current exec email.")

        if authenticated_user_title:
            logger.info("https://bing.com is authenticated.")
            return True

    except selenium.common.exceptions.TimeoutException:
        logger.critical("id_n element is not available on page.")
        return False

    return False
