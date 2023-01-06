import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import custom_logging
import util


def complete_more_promotion_this_or_that(*, browser: WebDriver, cardNumber: int):
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not util.waitUntilQuizLoads(browser):
        logger.critical("Quiz did not load. Resetting tabs and exiting module")
        raise Exception("Forced exception due to missing quiz load.")
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    util.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    logger.info("Looping questions. Range 10")
    for question in range(10):
        logger.info(f"Question {question} / 10")
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = util.getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = util.getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if answer1Code == correctAnswerCode:
            answer1.click()
            time.sleep(8)
        elif answer2Code == correctAnswerCode:
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    browser.close()
    time.sleep(2)
    logger.info("Returning to main window")
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)
