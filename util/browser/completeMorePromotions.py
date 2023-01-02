import logging

import util
from selenium.webdriver.chrome.webdriver import WebDriver

def complete_additional_promotions(browser: WebDriver, base_url: str):
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    morePromotions = util.getDashboardData(browser)['morePromotions']
    i = 0
    logger.info("Looping promotions")
    for promotion in morePromotions:
        try:
            i += 1
            if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                if promotion['promotionType'] == "urlreward":
                    logger.info("Incomplete promotion detected: url reward")
                    util.complete_more_promotion_search(browser=browser, cardNumber=i)
                elif promotion['promotionType'] == "quiz" and promotion['pointProgress'] == 0:
                    logger.info("Incomplete promotion detected: quiz")
                    if promotion['pointProgressMax'] == 10:
                        util.complete_more_promotion_abc(browser=browser, cardNumber=i)
                    elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                        util.complete_more_promotion_quiz(browser=browser, cardNumber=i, base_url=base_url)
                    elif promotion['pointProgressMax'] == 50:
                        util.complete_more_promotion_this_or_that(browser=browser, cardNumber=i, base_url=base_url)
                else:
                    if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                        util.complete_more_promotion_search(browser=browser, cardNumber=i)
        except Exception as e:
            logger.critical(f"Unexpected error in single additional promotion loop {e}")
            util.resetTabs(browser, BASE_URL=base_url)
