import random
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import custom_logging
import util


def exec_single_punch_card_child_promotion(
    browser: WebDriver, url: str, childPromotions: list["util.PunchCardChildPromotion"]
):
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(
        console=True, colors=True
    )
    logger.info(f"Navigating to punch card url: {url}")
    browser.get(url)
    time.sleep(2)
    childPromotions.pop(0)
    for childPromotion in childPromotions:
        logger.info("Completing single punch card childPromotion")
        if not childPromotion.complete:
            if childPromotion.promotionType == "urlreward":
                browser.find_elements(By.CLASS_NAME, "offer-cta")[1].find_element(
                    By.TAG_NAME, "button"
                ).click()
                time.sleep(1)
                browser.switch_to.window(window_name=browser.window_handles[1])
                time.sleep(random.randint(13, 17))
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name=browser.window_handles[0])
                time.sleep(2)

            if childPromotion.promotionType == "quiz":
                continue
                browser.find_elements(By.CLASS_NAME, "offer-cta")[0].find_element(
                    By.TAG_NAME, "button"
                ).click()  # click punch card button

                time.sleep(1)
                browser.switch_to.window(
                    window_name=browser.window_handles[1]
                )  # move browser to newly opened tab
                time.sleep(8)  # waiting for quiz to load
                pointsMax = int(browser.find_element(By.CLASS_NAME, "rqMCredits").text)

                numberOfQuestions = int(pointsMax / 10)

                for question in range(numberOfQuestions):
                    browser.execute_script(
                        "document.evaluate(\"//*[@id='QuestionPane"
                        + str(question)
                        + "']/div[1]/div[2]/a["
                        + str(random.randint(1, 3))
                        + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()'
                    )
                    time.sleep(5)
                    browser.find_element(
                        By.XPATH,
                        '//*[@id="AnswerPane'
                        + str(question)
                        + '"]/div[1]/div[2]/div[4]/a/div/span/input',
                    ).click()
                    time.sleep(3)

                time.sleep(5)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name=browser.window_handles[0])
                time.sleep(2)
