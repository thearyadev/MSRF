import random
import time

from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoAlertPresentException,
                                        NoSuchElementException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import util


def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    try:
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        util.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
    except (NoSuchElementException, TimeoutException):
        try:
            counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[
                      :-1][1:]
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
            return
        except NoSuchElementException:
            time.sleep(random.randint(5, 9))
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(2)
            return
    time.sleep(3)
    correctAnswer = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
    if browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
        browser.find_element(By.ID, "rqAnswerOption0").click()
    else:
        browser.find_element(By.ID, "rqAnswerOption1").click()
    time.sleep(10)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)
