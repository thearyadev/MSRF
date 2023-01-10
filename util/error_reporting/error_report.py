import datetime
import io
import json
import sys
import traceback
import zipfile

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util

from ..browser.getDashboardData import load_dashboard_data
from ..models.dashboard_data import DashboardData
from .json_encoder import DateTimeEncoder

logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)


class ErrorReport:
    """Data structure to hold information about a single error report."""

    def __init__(self, *, screenshot: bytes, accountDataJson: str, url: str, html: str, exceptionData: str):
        self.screenshot: bytes = screenshot
        self.accountDataJson: str = accountDataJson
        self.url: str = url
        self.html: str = html
        self.exceptionData: str = exceptionData
        self.compressed: bool = False
        self.data: bytes = bytes()
        self.file_path: str = str()

    def compress(self) -> 'ErrorReport':
        """
        Compresses all the data in the error report into a zipfile byte buffer
        Returns self
        data is stored in self.data
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer,
                             "a",
                             zipfile.ZIP_DEFLATED,
                             False) as zip_file:
            zip_file.writestr("screenshot.png", self.screenshot)
            zip_file.writestr("account_data.json", self.accountDataJson)
            zip_file.writestr("url.txt", self.url)
            zip_file.writestr("page.html", self.html)
            zip_file.writestr("traceback.txt", self.exceptionData)
        self.data = zip_buffer.getvalue()
        self.compressed = True
        return self


class ErrorReporter:
    """Handles error reporting data collection"""

    def __init__(self, error_dir: str = "./errors"):
        self._err_dir: str = error_dir

    @staticmethod
    def _get_browser_screenshot(browser: WebDriver) -> bytes:
        """uses the webdriver at the time of the exception and takes a screenshot"""
        return browser.get_screenshot_as_png()

    @staticmethod
    def _get_html(browser: WebDriver) -> str:
        """uses the webdriver at the time of the exception and gets the page source"""
        return browser.execute_script("return document.body.innerHTML")

    @staticmethod
    def _get_current_url(browser: WebDriver) -> str:
        """uses the webdriver at the time of the exception and gets the url"""
        return browser.current_url

    @staticmethod
    def _serialize_dashboard_data_as_json(browser: WebDriver, accountData: util.DashboardData | None | str) -> str:
        """
        Converts the account data to a json string
        The accountData parameter has multiple types to accept different states of errors.
        Browser errors can happen:
        1. when the accountData is the cause of the exception (None)
        2. when the instance is not authenticated. There is no dashboard if the account is not logged in.(None)
        3. When the accountData is not available at the time of the exception (str("RETRIEVE"))
            - the process of retrieving the accountData would change the location of the browser
              this would prevent a useful screenshot from being taken
            - the account data is "RETRIEVE" later, instead of at the time this class is instantiated.
        4. When the accountData was available at the time of the exception
        """
        if isinstance(accountData, str):
            if accountData == "RETRIEVE":
                try:
                    accountData = load_dashboard_data(browser)
                except Exception:
                    return str(None)
        if accountData is None:
            return str(None)
        # use encoder to serialize datetime.datetime keys -> str
        return json.dumps(obj=accountData.dict(), cls=DateTimeEncoder)

    @staticmethod
    def _parse_exception(exception: Exception) -> str:
        try:
            return ''.join(traceback.format_exception(*sys.exc_info()))
        except Exception:
            return ''.join(traceback.format_exception(exception))

    def generate_report(self, browser: WebDriver, accountData: DashboardData | None | str,
                        exception: Exception) -> ErrorReport:
        try:
            report = ErrorReport(
                screenshot=self._get_browser_screenshot(browser),
                html=self._get_html(browser),
                url=self._get_current_url(browser),
                accountDataJson=self._serialize_dashboard_data_as_json(browser, accountData),
                exceptionData=self._parse_exception(exception)
            ).compress()
            self._write(report)  # write to disk
        except Exception as err:  # if there's an error, just skip making the error report.
            logger.critical(f"Unable to create error report. Unknown error {err}")
        else:
            return report  # if no errors, send the report back to the user.

    def _write(self, report: ErrorReport) -> None:
        report.file_path = self._err_dir + f"/error_{datetime.datetime.now().timestamp()}.zip"  # save filename
        with open(report.file_path, "wb") as file:
            file.write(report.data)  # write
