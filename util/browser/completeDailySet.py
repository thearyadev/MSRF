import logging

import util
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
import urllib.parse
from util import deprecated


@deprecated
def complete_daily_set(browser: WebDriver, base_url: str):
    """
    Completes the daily set of an authenticated microsoft account.
    """
    logger: logging.Logger = logging.getLogger("msrf")  # get logger

    # load the data from dashboard.
    d = util.get_dashboard_data(browser)['dailySetPromotions']

    logger.info("Successfully loaded correct dashboard data.")

    # Get the current date
    todayDate = datetime.today().strftime('%m/%d/%Y')
    todayPack = []
    # load all items for today.
    for date, data in d.items():
        if date == todayDate:
            todayPack = data

    # iter things that can be done today.
    for activity in todayPack:
        try:
            if activity['complete'] == False:
                cardNumber = int(activity['offerId'][-1:])  # get card number
                if activity['promotionType'] == "urlreward":  # check promotion type
                    logger.info(f"Completing search of card {cardNumber}")
                    util.complete_daily_set_search(browser, cardNumber)  # exec

                if activity['promotionType'] == "quiz":  # check promotion type
                    # This block handles quizzes. Quizzes have a max score and a current score,
                    # as they don't need to be done all at once.
                    # check the score values and determine which quiz function needs to be executed.
                    if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                        logger.info(f"Completing This or That of card {cardNumber}")
                        util.complete_daily_set_this_or_that(browser, cardNumber, base_url=base_url)

                    elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity[
                        'pointProgress'] == 0:
                        logger.info(f"Completing quiz of card {cardNumber}")
                        util.complete_daily_set_quiz(browser, cardNumber, base_url=base_url)

                    elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                        searchUrl = urllib.parse.unquote(
                            urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                        searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for filter in searchUrlQueries['filters'][0].split(" "):
                            filter = filter.split(':', 1)
                            filters[filter[0]] = filter[1]
                        if "PollScenarioId" in filters:
                            logger.info(f"Completing poll of card: {cardNumber}")
                            util.completeDailySetSurvey(browser, cardNumber)
                        else:
                            logger.info(f"Completing quiz of card: {cardNumber}")
                            util.completeDailySetVariableActivity(browser, cardNumber)
        except Exception as e:
            logger.critical(f"Unknown exception was raised in daily set module. {e}")
            util.resetTabs(browser, base_url)


def exec_daily_set(browser: WebDriver):
    """Completes the daily set section"""
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    #accountData: util.DashboardData = util.load_dashboard_data(browser)
    # load the daily set data.
    with open("../../dashboard_data_schema_source.json", "r") as file:
        import json
        accountData = util.DashboardData(**json.load(file))
        print(accountData.dailySetPromotions)
    todayDate = datetime.today().strftime('%m/%d/%Y')


if __name__ == '__main__':
    exec_daily_set(0)