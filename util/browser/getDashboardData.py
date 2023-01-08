import time

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util
import typing

if typing.TYPE_CHECKING:
    from util import ErrorReport, ErrorReporter

from ..models.dashboard_data import DashboardData


def load_dashboard_data(browser: WebDriver) -> DashboardData | None:
    from util import ErrorReport, ErrorReporter
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(colors=True, console=True)
    logger.info("loading dashboard data")
    browser.get("https://rewards.bing.com")
    time.sleep(3)
    try:
        return util.DashboardData(**browser.execute_script("return dashboard"))
    except Exception as e:
        # Since this is breaking, it may be ideal to exit the thread with sys.exit(). tbd.
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData=None,
            exception=e
        )
        logger.critical("Unable to load dashboard data.  "
                        f"Error report has been generated: {errorReport.file_path}")
