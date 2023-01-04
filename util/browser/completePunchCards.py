import logging

import custom_logging
import util

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time
from util import deprecated


@deprecated
def complete_punch_cards(browser: WebDriver, base_url: str):
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    punchCards = util.getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        try:
            if punchCard['parentPromotion'] != None and \
                    punchCard['childPromotions'] != None and \
                    punchCard['parentPromotion']['complete'] == False and \
                    punchCard['parentPromotion']['pointProgressMax'] != 0:
                if base_url == "https://rewards.microsoft.com":
                    logger.info("Completing single punch card")
                    util.complete_punch_card(browser, punchCard['parentPromotion']['attributes']['destination'],
                                             punchCard['childPromotions'])
                else:
                    url = punchCard['parentPromotion']['attributes']['destination']
                    path = url.replace(
                        'https://account.microsoft.com/rewards/dashboard/', '')
                    userCode = path[:4]
                    dest = 'https://account.microsoft.com/rewards/dashboard/' + \
                           userCode + path.split(userCode)[1]
                    util.complete_punch_card(browser, url, punchCard['childPromotions'])
        except Exception as e:
            logger.critical(f"Uncaught exception in completing punch cards. Likely malformed data. Resetting tabs. {e}")
            util.resetTabs(browser, BASE_URL=base_url)
    time.sleep(2)
    logger.info("Returning home.")
    browser.get(base_url)
    time.sleep(2)


def exec_punch_cards(browser: WebDriver):
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)

    accountData: util.DashboardData = util.load_dashboard_data(browser)
    if accountData is None:
        logging.critical("Unable to complete punch cards due to missing dashboard data.")
        return

    punch_cards: list[util.PunchCards] = accountData.punchCards

    if not punch_cards:
        logging.critical("Unable to complete punch cards. Attribute is None or Empty Array")
        return

    for punch_card in punch_cards:
        if punch_card.parentPromotion is not None \
                and punch_card.childPromotion is not None \
                and not punch_card.parentPromotion.complete \
                and punch_card.parentPromotion.pointProgressMax != 0:
            logger.info(f"Valid punch card child promotion found: {punch_card.name}")
            try:
                util.exec_single_punch_card_child_promotion(
                    browser,
                    punch_card.parentPromotion.destinationUrl,
                    punch_card.childPromotion
                )
            except Exception as e:
                logging.critical(f"Failed to complete punch card child promotion. Expected error: {e}")
            else:
                logger.info(f"Successfully completed punch card child promotion: {punch_card.name}")
