import logging

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util


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
