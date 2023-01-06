import sys
from subprocess import CREATE_NO_WINDOW
import atexit

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging


def init_browser(*, headless: bool, agent: str) -> WebDriver:
    """
    Initializes a new Chrome instance using Selenium and chromedriver.

    :headless browser operation mode. Headless will not display a window.
    :agent mobile or pc agent string.
    :config generic config for this application.
    """
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    options = Options()
    options.add_argument("user-agent=" + agent)
    options.add_argument("log-level=3")
    if headless:
        options.add_argument("--headless")

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        logger.info("Starting browser in bundled mode")
        options.binary_location = "bin/chrome/chrome.exe"
        options.add_argument("--log-level=OFF")
        args = ["hide_console", ]

        service = Service("bin/chromedriver.exe", service_args=args)
        service.creation_flags = CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=options)
        atexit.register(driver.quit)
        return driver

    else:
        logger.info("Starting browser in development mode")
        driver = webdriver.Chrome(options=options)
        atexit.register(driver.quit)
        return driver
