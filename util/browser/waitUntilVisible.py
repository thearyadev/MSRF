import typing

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import custom_logging

if typing.TYPE_CHECKING:
    pass


def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    from util import ErrorReport, ErrorReporter
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    try:
        WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))
    except Exception as e:
        errorReport: ErrorReport = ErrorReporter().generate_report(
            browser,
            accountData="RETRIEVE",
            exception=e
        )
        logger.critical(f"Error report has been generated: {errorReport.file_path}")
        return
