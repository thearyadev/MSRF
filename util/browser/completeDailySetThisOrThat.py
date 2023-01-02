import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import util
from util import deprecated
import logging


def getAnswerCode(key: str, string: str) -> str:
    t = 0
    for i in range(len(string)):
        t += ord(string[i])
    t += int(key[-2:], 16)
    return str(t)




def complete_daily_set_this_or_that(browser: WebDriver, cardNumber: int, base_url: str):
    """
    Completes the this or that quiz.
    """

    logger: logging.Logger = logging.getLogger("msrf")

    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not util.waitUntilQuizLoads(browser):
        util.resetTabs(browser, base_url)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    util.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if answer1Code == correctAnswerCode:
            answer1.click()
            time.sleep(8)
        elif answer2Code == correctAnswerCode:
            answer2.click()
            time.sleep(8)
        logger.info("Question answered")
    time.sleep(5)
    browser.close()
    time.sleep(2)
    logger.info("Switching back to main window.")
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

