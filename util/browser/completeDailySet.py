import logging

import util
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
import urllib.parse
from util import deprecated
from rich import print


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


# noinspection PyTypeChecker
def exec_daily_set(browser: WebDriver):
    """Completes the daily set section"""
    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    accountData: util.DashboardData = util.load_dashboard_data(browser)
    if accountData is None:
        logging.critical("Unable to complete daily set due to missing dashboard data.")
        return
    # load the daily set data.
    
    # the daily set is a few quizzes and such for the current date.
    # the data will include a dictionary of "dates". yesterday, today, and tomorrow.
    # only Today is can be done.
    # from this dict, get the one from today.

    # Get the current date. Parsed date has no time, replace all times with 0
    # get data from dict. Will return None if there is no daily set.
    daily_set: list[util.DailyPromotion] | None = accountData.dailySetPromotions.get(
        datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
    )

    if daily_set is None:
        logger.warning("Daily set did not yield any results. Dictionary containing the data does not contain the key "
                       "for the current date.")
        return

    # if daily set was found
    # iterate over all items of the daily set.

    for daily_set_item in daily_set:
        if not daily_set_item.complete:  # if the item hasn't been done yet
            logger.info(f"Completing Daily Set Card #{daily_set_item.cardNumber}")

            if daily_set_item.promotionType == "urlreward":
                logger.info("Daily set item is of type [urlreward]")
                try:
                    logger.info(f"Completing daily set search for card #{daily_set_item.cardNumber}")
                    util.complete_daily_set_search(browser, daily_set_item.cardNumber)
                except Exception as e:
                    logger.critical(f"Unable to complete daily_set_search due to an uncaught error in scraper. {e}")

            if daily_set_item.promotionType == "quiz":
                logger.info("Daily set item is of type [quiz]")
                if daily_set_item.pointProgressMax == 50 and daily_set_item.pointProgress == 0:
                    # if the point progress max is 50, it is a this_or_that quiz.
                    # only complete if the pointProgress is == 0 (untouched)
                    logger.info(f"Completing this or that for card #{daily_set_item.cardNumber}")
                    try:
                        util.complete_daily_set_this_or_that(browser, daily_set_item.cardNumber,
                                                             base_url="https://rewards.bing.com")
                    except Exception as e:
                        logger.critical(
                            f"Unable to complete daily_set_this_or_that due to an uncaught error in scraper. {e}")
                elif daily_set_item.pointProgressMax in (40, 30) and daily_set_item.pointProgressMax == 0:
                    # if the max points are 40 or 30, it is just a generic quiz
                    # only attempt if progress on the quiz is 0
                    logger.info(f"Completing quiz of card #{daily_set_item.cardNumber}")
                    try:
                        util.complete_daily_set_quiz(browser,
                                                     daily_set_item.cardNumber,
                                                     base_url="https://rewards.bing.com")
                    except Exception as e:
                        logger.critical(
                            f"Unable to complete daily_set_quiz due to an uncaught error in scraper. {e}")

                elif daily_set_item.pointProgressMax == 10 and daily_set_item.pointProgress == 0:
                    # if the total point value is 10 and the point progress is 0 (untouched)
                    # this block is legacy code. Not sure what it does exactly, but it remains here in case it breaks
                    try:
                        searchUrl = urllib.parse.unquote(
                            urllib.parse.parse_qs(
                                # url query params dict
                                # get ru, then first element of a list
                                urllib.parse.urlparse(daily_set_item.destinationUrl).query)['ru'][0]

                        )
                        # something?
                        searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for fltr in searchUrlQueries['filters'][0].split(" "):
                            fltr = fltr.split(':', 1)
                            filters[fltr[0]] = fltr[1]
                        if "PollScenarioId" in filters:
                            logger.info(f"Completing poll of card #{daily_set_item.cardNumber}")
                            try:
                                util.completeDailySetSurvey(browser, daily_set_item.cardNumber)
                            except Exception as e:
                                logger.critical(
                                    f"Unable to complete daily_set_survey due to an uncaught error in scraper. {e}")
                        else:
                            logger.info(f"Completing quiz of card #{daily_set_item.cardNumber}")
                            try:
                                util.completeDailySetVariableActivity(browser, daily_set_item.cardNumber)
                            except Exception as e:
                                logger.critical(
                                    f"Unable to complete daily_set_variable_activity due to an uncaught error in "
                                    f"scraper. {e}")
                    except Exception as e:
                        logger.critical(f"Legacy code segment caused an exception. {e}")
        else:
            logger.info(f"Daily Set Card #{daily_set_item.cardNumber} is already complete")