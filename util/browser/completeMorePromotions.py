import logging

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util
import typing

if typing.TYPE_CHECKING:
    from util import ErrorReport, ErrorReporter


def exec_additional_promotions(browser: WebDriver):
    from util import ErrorReport, ErrorReporter
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    accountData: util.DashboardData = util.load_dashboard_data(browser)

    more_promotions: list[util.MorePromotion] = accountData.morePromotions

    if accountData is None:
        logging.critical("Unable to complete more promotions due to missing dashboard data.")
        return

    if not more_promotions:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=accountData,
            exception=Exception("Manual exception. Missing more_promotions dashboard data")
        )
        logging.critical("Unable to complete more promotions. Attribute is None or Empty Array"
                         f"Error report generated: {errorReport.file_path}")
        return

    for cardNumberNoOffset, promotion in enumerate(more_promotions):
        cardNo = cardNumberNoOffset + 1
        try:
            if not promotion.complete and promotion.pointProgressMax != 0:
                if promotion.promotionType == "urlreward":
                    logger.info("More promotion type [urlreward] eligible")
                    try:
                        util.complete_more_promotion_search(browser=browser, cardNumber=cardNo)
                    except Exception as e:
                        errorReport: ErrorReport = ErrorReporter().generate_report(
                            browser,
                            accountData=accountData,
                            exception=e
                        )
                        logger.critical("Uncaught error in more promotions scraper. "
                                        f"Error report has been generated: {errorReport.file_path}")

                elif promotion.promotionType == "quiz" and promotion.pointProgress == 0:
                    logger.info("More promotion type [quiz] eligible")
                    if promotion.pointProgressMax == 10:
                        logger.info("Promotion Point Quiz value: 10")
                        try:
                            util.complete_more_promotion_abc(browser=browser, cardNumber=cardNo)
                        except Exception as e:
                            errorReport: ErrorReport = ErrorReporter().generate_report(
                                browser,
                                accountData=accountData,
                                exception=e
                            )
                            logger.critical("Uncaught error in more promotions scraper. "
                                            f"Error report has been generated: {errorReport.file_path}")

                    elif promotion.pointProgressMax in (30, 40) and not promotion.complete:
                        logger.info("Promotion Point Quiz value: 30 or 40")

                        try:
                            util.complete_more_promotion_quiz(browser=browser, cardNumber=cardNo)
                        except Exception as e:
                            errorReport: ErrorReport = ErrorReporter().generate_report(
                                browser,
                                accountData=accountData,
                                exception=e
                            )
                            logger.critical("Uncaught error in more promotions scraper. "
                                            f"Error report has been generated: {errorReport.file_path}")

                    elif promotion.pointProgressMax == 50:
                        logger.info("Promotion Point Quiz value: 50")

                        try:
                            util.complete_more_promotion_this_or_that(browser=browser, cardNumber=cardNo)
                        except Exception as e:
                            errorReport: ErrorReport = ErrorReporter().generate_report(
                                browser,
                                accountData=accountData,
                                exception=e
                            )
                            logger.critical("Uncaught error in more promotions scraper. "
                                            f"Error report has been generated: {errorReport.file_path}")
                else:
                    if promotion.pointProgressMax in (100, 200):
                        logger.info("Promotion Point Search value: 100-200")
                        try:
                            util.complete_more_promotion_search(browser=browser, cardNumber=cardNo)
                        except Exception as e:
                            errorReport: ErrorReport = ErrorReporter().generate_report(
                                browser,
                                accountData=accountData,
                                exception=e
                            )
                            logger.critical("Uncaught error in more promotions scraper. "
                                            f"Error report has been generated: {errorReport.file_path}")
        except Exception as e:
            errorReport: ErrorReport = ErrorReporter().generate_report(
                browser,
                accountData=accountData,
                exception=e
            )
            logger.critical("Uncaught error in more promotions scraper. "
                            f"Error report has been generated: {errorReport.file_path}")
