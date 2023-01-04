import json
import logging

from pydantic import BaseModel

import custom_logging
import util
from selenium.webdriver.chrome.webdriver import WebDriver
from util import deprecated


@deprecated
def getRemainingSearches(browser: WebDriver):
    dashboard = util.getDashboardData(browser)
    searchPoints = 1
    counters = dashboard['userStatus']['counters']
    if not 'pcSearch' in counters:
        return 0, 0
    progressDesktop = counters['pcSearch'][0]['pointProgress'] + counters['pcSearch'][1]['pointProgress']
    targetDesktop = counters['pcSearch'][0]['pointProgressMax'] + counters['pcSearch'][1]['pointProgressMax']
    if targetDesktop == 33:
        # Level 1 EU
        searchPoints = 3
    elif targetDesktop == 55:
        # Level 1 US
        searchPoints = 5
    elif targetDesktop == 102:
        # Level 2 EU
        searchPoints = 3
    elif targetDesktop >= 170:
        # Level 2 US
        searchPoints = 5
    remainingDesktop = int((targetDesktop - progressDesktop) / searchPoints)
    remainingMobile = 0
    if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
        progressMobile = counters['mobileSearch'][0]['pointProgress']
        targetMobile = counters['mobileSearch'][0]['pointProgressMax']
        remainingMobile = int((targetMobile - progressMobile) / searchPoints)
    return remainingDesktop, remainingMobile


class RemainingSearchOutline(BaseModel):
    pcSearches: int = 0
    mobileSearches: int = 0


def get_remaining_searches(browser: WebDriver) -> RemainingSearchOutline:
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)

    accountData: util.DashboardData = util.load_dashboard_data(browser)

    counters: util.Counters = accountData.userStatus.counters
    remainingSearches: RemainingSearchOutline = RemainingSearchOutline()

    if not accountData:
        logger.critical("Dashboard data could not be loaded.")
        return remainingSearches

    if not counters.pcSearch and not counters.mobileSearch:  # if none or empty array
        logger.critical("Counters may be missing. valued at zero")
        return remainingSearches
    # pc searches = points required - points earned
    remainingSearches.pcSearches = int((counters.pcSearch[0].pointProgressMax - counters.pcSearch[0].pointProgress) / 3)
    remainingSearches.mobileSearches = \
        int((counters.mobileSearch[0].pointProgressMax - counters.mobileSearch[0].pointProgress) / 3)
    return remainingSearches
