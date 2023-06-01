import typing

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util

if typing.TYPE_CHECKING:
    pass


def getPointCount(browser: WebDriver) -> int:
    """
    Navigates to bing.com as an authenticated user. Gets the point count and returns it.
    Defaults to 0 if the function fails.
    :browser Selenium web driver
    """
    from util import ErrorReport, ErrorReporter

    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(
        console=True, colors=True
    )
    accountData = util.load_dashboard_data(browser)

    if not accountData:
        logger.critical("Account data is missing. Unable to get point count")
        return 0
    try:
        return accountData.userStatus.availablePoints
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser, accountData="RETRIEVE", exception=e
        )
        logger.critical(
            "Failed to complete PC bing searches. "
            f"Error report has been generated: {errorReport.file_path}"
        )
        logger.critical(f"Unexpected error in point retrieval. {e}")
    return 0
