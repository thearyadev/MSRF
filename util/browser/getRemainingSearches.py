from pydantic import BaseModel

import custom_logging
import util
from selenium.webdriver.chrome.webdriver import WebDriver


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
    try:
        remainingSearches.pcSearches = int(
            (counters.pcSearch[0].pointProgressMax - counters.pcSearch[0].pointProgress) / 3)
    except TypeError:
        pass
    try:
        remainingSearches.mobileSearches = \
            int((counters.mobileSearch[0].pointProgressMax - counters.mobileSearch[0].pointProgress) / 3)
    except TypeError:
        pass

    return remainingSearches
