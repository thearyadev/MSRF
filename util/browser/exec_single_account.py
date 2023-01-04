import datetime
import threading

import selenium.common.exceptions

import custom_logging
import util
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import database
import logging


def exec_farmer(*, account: util.MicrosoftAccount, config: util.Config, db: database.DatabaseAccess):
    """
    Runs the script on a single MicrosoftAccount object.

    :account MicrosoftAccount object
    :config generic configuration for this project
    :db DatabaseAccess class to record MicrosoftAccount changes
    """

    account.lastExec = datetime.datetime.now(tz=datetime.timezone.utc)
    db.write(account=account)

    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)

    # init browser
    logger.info(f"Current Account: {account}")
    # Defaults in headless mode.
    # Starting with PC user agent

    # if debug is TRUE, run headless=FALSE to view the browser window.
    browser: WebDriver = util.init_browser(headless=not config.debug, agent=config.pc_user_agent)

    logger.info("Attempting login...")
    # go through login process
    login_state = util.authenticate_microsoft_account(browser=browser,
                                                      account=account)
    if not login_state:
        logger.critical("Login failed. Module may be broken, or credentials are invalid.")
        return

    logger.info("Successfully authenticated. ")
    logger.info("Navigating to https://account.microsoft.com/")
    browser.get('https://account.microsoft.com/')
    try:
        util.waitUntilVisible(browser, By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a', 20)
    except selenium.common.exceptions.TimeoutException:
        logger.error("Unable to confirm if page has loaded. Continuing anyway...")

    # Check if the current page is valid.
    BASE_URL = 'https://rewards.microsoft.com'
    if not util.isMicrosoftRewards(browser):
        BASE_URL = 'https://account.microsoft.com/rewards'
        browser.get(BASE_URL)

    account.points = util.getPointCount(browser)  # will redirect to bing.com. Go back to baseurl
    db.write(account)
    logger.info(f"Current Points: {account.points}")

    browser.get(BASE_URL)  # return

    # Farmer start
    logger.info("Setup complete. Starting point collection process.")

    # daily set
    logger.info("(1/5) Completing DAILY SET")
    try:
        util.exec_daily_set(browser)
    except Exception as e:
        util.resetTabs(browser, BASE_URL)
        logger.critical(f"Uncaught exception has caused daily set to fail. {e}")
    else:
        logger.info("Successfully completed DAILY SET")

    account.points = util.getPointCount(browser)
    db.write(account)
    # punch cards

    logger.info("(2/5) Completing PUNCH CARDS")
    try:
        util.exec_punch_cards(browser)
    except Exception as e:
        util.resetTabs(browser, BASE_URL)
        logger.critical(f"Uncaught exception has caused punch cards to fail. {e}")
    else:
        logger.info("Successfully completed PUNCH CARDS")

    account.points = util.getPointCount(browser)
    db.write(account)

    # additional promotions
    logger.info("(3/5) Completing ADDITIONAL PROMOTIONS")
    try:
        util.complete_additional_promotions(browser, base_url=BASE_URL)
    except Exception as e:
        util.resetTabs(browser, BASE_URL)
        logger.critical(f"Uncaught exception has caused additional promotions to fail. {e}")
    else:
        logger.info("Successfully completed ADDITIONAL PROMOTIONS")

    # update points
    account.points = util.getPointCount(browser)
    db.write(account)

    # bing searches.
    try:
        remainingSearches: util.RemainingSearchOutline = util.get_remaining_searches(browser)
    except Exception as e:
        logger.critical(f"Unable to get remaining searches. Could be malformed data. {e}")
    else:
        logger.info(f"Searches loaded. {remainingSearches}")

        if remainingSearches.pcSearches:
            account.points = util.getPointCount(browser)
            db.write(account)
            searchTerms = util.getGoogleTrends(remainingSearches.pcSearches, config.LANG, config.GEO)
            try:
                util.exec_bing_searches(
                    browser=browser,
                    searchCount=remainingSearches.pcSearches,
                    terms=searchTerms,
                    starting_points=account.points,
                    agent=config.pc_user_agent,
                    mobile=False
                )
            except Exception as e:
                logger.critical(f"Failed to complete PC bing searches. {e}")

        if remainingSearches.mobileSearches:
            logging.info("Starting mobile browser.")
            account.points = util.getPointCount(browser)
            db.write(account)
            mobileBrowser = util.init_browser(headless=not config.debug, agent=config.mobile_user_agent)
            util.authenticate_microsoft_account(browser=mobileBrowser, account=account)
            searchTerms = util.getGoogleTrends(remainingSearches.mobileSearches, config.LANG, config.GEO)
            try:
                util.exec_bing_searches(
                    browser=mobileBrowser,
                    searchCount=remainingSearches.mobileSearches,
                    terms=searchTerms,
                    starting_points=account.points,
                    agent=config.mobile_user_agent,
                    mobile=True
                )
            except Exception as e:
                logger.critical(f"Failed to complete Mobile bing searches. {e}")
            logger.info("Closing mobile browser")
            mobileBrowser.quit()

    logging.info("Getting closing point count.")
    account.points = util.getPointCount(browser)
    db.write(account)

    logger.info(F"Closing Point Total: {account.points}")
    logger.info("Closing main browser.")
    browser.quit()
