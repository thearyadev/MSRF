import logging

import custom_logging
import util

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time
from util import deprecated


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
