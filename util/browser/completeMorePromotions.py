import json
import logging

import custom_logging
import util
from selenium.webdriver.chrome.webdriver import WebDriver
from util import deprecated


@deprecated
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


def exec_additional_promotions(browser: WebDriver):
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    accountData: util.DashboardData = util.load_dashboard_data(browser)

    more_promotions: list[util.MorePromotion] = accountData.morePromotions

    if accountData is None:
        logging.critical("Unable to complete more promotions due to missing dashboard data.")
        return

    if not more_promotions:
        logging.critical("Unable to complete more promotions. Attribute is None or Empty Array")
        return

    for cardNumberNoOffset, promotion in enumerate(more_promotions):
        promotion.complete = False
        promotion.pointProgress = 0
        cardNo = cardNumberNoOffset + 1
        try:
            if not promotion.complete and promotion.pointProgressMax != 0:
                if promotion.promotionType == "urlreward":
                    logger.info("More promotion type [urlreward] eligible")
                    util.complete_more_promotion_search(browser=browser, cardNumber=cardNo)
                elif promotion.promotionType == "quiz" and promotion.pointProgress == 0:
                    logger.info("More promotion type [quiz] eligible")
                    print("More promotion type [quiz] eligible")
                    if promotion.pointProgressMax == 10:
                        logger.info("Promotion Point Quiz value: 10")
                        util.complete_more_promotion_abc(browser=browser, cardNumber=cardNo)
                    elif promotion.pointProgressMax in (30, 40):
                        logger.info("Promotion Point Quiz value: 30 or 40")
                        util.complete_more_promotion_quiz(browser=browser, cardNumber=cardNo)
                    elif promotion.pointProgressMax == 50:
                        logger.info("Promotion Point Quiz value: 50")
                        util.complete_more_promotion_this_or_that(browser=browser, cardNumber=cardNo)
                else:
                    if promotion.pointProgressMax in (100, 200):
                        logger.info("Promotion Point Search value: 100-200")
                        util.complete_more_promotion_search(browser=browser, cardNumber=cardNo)
        except Exception as e:
            logger.critical(f"Uncaught error in more promotions scraper. {e}")
