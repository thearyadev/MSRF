import typing
import urllib.parse
from datetime import datetime

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util

if typing.TYPE_CHECKING:
    pass


# noinspection PyTypeChecker
def exec_daily_set(browser: WebDriver):
    """Completes the daily set section"""
    from util import ErrorReport, ErrorReporter
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    accountData: util.DashboardData = util.load_dashboard_data(browser)
    if accountData is None:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=accountData,
            exception=Exception("Manual exception. Dashboard is missing")
        )
        logger.critical("Unable to complete daily set due to missing dashboard data."
                        f"Error report has been generated: {errorReport.file_path}")
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
                    errorReport: ErrorReport = ErrorReporter().generate_report(
                        browser,
                        accountData=accountData,
                        exception=e
                    )
                    logger.critical("Unable to complete daily_set_search due to an uncaught error in scraper."
                                    f"Error report has been generated: {errorReport.file_path}")

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
                        errorReport: ErrorReport = ErrorReporter().generate_report(
                            browser,
                            accountData=accountData,
                            exception=e
                        )
                        logger.critical("Unable to complete daily_set_this_or_that due to an uncaught error in scraper."
                                        f"Error report has been generated: {errorReport.file_path}")
                elif daily_set_item.pointProgressMax in (40, 30) and daily_set_item.pointProgressMax == 0:
                    # if the max points are 40 or 30, it is just a generic quiz
                    # only attempt if progress on the quiz is 0
                    logger.info(f"Completing quiz of card #{daily_set_item.cardNumber}")
                    try:
                        util.complete_daily_set_quiz(browser,
                                                     daily_set_item.cardNumber,
                                                     base_url="https://rewards.bing.com")
                    except Exception as e:
                        errorReport: ErrorReport = ErrorReporter().generate_report(
                            browser,
                            accountData=accountData,
                            exception=e
                        )
                        logger.critical("Unable to complete daily_set_quiz due to an uncaught error in scraper."
                                        f"Error report has been generated: {errorReport.file_path}")

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
                                errorReport: ErrorReport = ErrorReporter().generate_report(
                                    browser,
                                    accountData=accountData,
                                    exception=e
                                )
                                logger.critical(
                                    "Unable to complete daily_set_survey due to an uncaught error in scraper. "
                                    f"Error report has been generated: {errorReport.file_path}")
                        else:
                            logger.info(f"Completing quiz of card #{daily_set_item.cardNumber}")
                            try:
                                util.completeDailySetVariableActivity(browser, daily_set_item.cardNumber)
                            except Exception as e:
                                errorReport: ErrorReport = ErrorReporter().generate_report(
                                    browser,
                                    accountData=accountData,
                                    exception=e
                                )
                                logger.critical(
                                    "UUnable to complete daily_set_variable_activity due to an uncaught error in "
                                    "scraper. "
                                    f"Error report has been generated: {errorReport.file_path}")
                    except Exception as e:
                        errorReport: ErrorReport = ErrorReporter().generate_report(
                            browser,
                            accountData=accountData,
                            exception=e
                        )
                        logger.critical("Legacy code segment caused an exception."
                                        f"Error report has been generated: {errorReport.file_path}")
        else:
            logger.info(f"Daily Set Card #{daily_set_item.cardNumber} is already complete")
