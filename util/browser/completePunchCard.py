import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time

import random
from util import deprecated
import util


@deprecated
def complete_punch_card(browser: WebDriver, url: str, childPromotions: dict):
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    logger.info(f"Navigating to punch card url: {url}")
    browser.get(url)
    for child in childPromotions:
        logger.info("Completing single childPromotion")
        if child['complete'] == False:
            if child['promotionType'] == "urlreward":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name=browser.window_handles[1])
                time.sleep(random.randint(13, 17))
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name=browser.window_handles[0])
                time.sleep(2)
            if child['promotionType'] == "quiz":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name=browser.window_handles[1])
                time.sleep(8)
                counter = str(
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][
                          1:]
                numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    browser.execute_script(
                        'document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(
                            random.randint(1,
                                           3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(
                        question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name=browser.window_handles[0])
                time.sleep(2)


def exec_single_punch_card_child_promotion(browser: WebDriver,
                                           url: str,
                                           childPromotions: list['util.PunchCardChildPromotion']):
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    logger.info(f"Navigating to punch card url: {url}")
    browser.get(url)

    for child in childPromotions:
        logger.info("Completing single childPromotion")
        if not child.complete:
            if child.promotionType == "urlreward":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name=browser.window_handles[1])
                time.sleep(random.randint(13, 17))
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name=browser.window_handles[0])
                time.sleep(2)
            if child.promotionType == "quiz":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name=browser.window_handles[1])
                time.sleep(8)
                counter = str(
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][
                          1:]
                numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    browser.execute_script(
                        'document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(
                            random.randint(1, 3)) \
                        + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(
                        question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name=browser.window_handles[0])
                time.sleep(2)
