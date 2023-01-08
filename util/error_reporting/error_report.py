import datetime
import io
import json
import traceback
import zipfile

from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
from ..models.dashboard_data import DashboardData
from ..browser.getDashboardData import load_dashboard_data
from .json_encoder import DateTimeEncoder
import util

logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)


class ErrorReport:
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
    def __init__(self, error_dir: str = "./errors"):
        self._err_dir: str = error_dir
        print("Error reporting started...")

    @staticmethod
    def _get_browser_screenshot(browser: WebDriver) -> bytes:
        return browser.get_screenshot_as_png()

    @staticmethod
    def _get_html(browser: WebDriver) -> str:
        return browser.execute_script("return document.body.innerHTML")

    @staticmethod
    def _get_current_url(browser: WebDriver) -> str:
        return browser.current_url

    @staticmethod
    def _serialize_dashboard_data_as_json(browser: WebDriver, accountData: util.DashboardData | None | str) -> str:
        if isinstance(accountData, str):
            if accountData == "RETRIEVE":
                try:
                    accountData = load_dashboard_data(browser)
                except Exception:
                    return str(None)
        if accountData is None:
            return str(None)

        return json.dumps(obj=accountData.dict(), cls=DateTimeEncoder)

    @staticmethod
    def _parse_exception(exception: Exception) -> str:
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
            self._write(report)
        except Exception as err:
            logger.critical(f"Unable to create error report. Unknown error {err}")
        else:
            return report

    def _write(self, report: ErrorReport) -> None:
        report.file_path = self._err_dir + f"/error_{datetime.datetime.now().timestamp()}.zip"
        with open(report.file_path, "wb") as file:
            file.write(report.data)
