import atexit
import subprocess
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

import custom_logging
import util


def init_browser_legacy(*, headless: bool, agent: str) -> WebDriver:
    """
    Initializes a new Chrome instance using Selenium and chromedriver.

    :headless browser operation mode. Headless will not display a window.
    :agent mobile or pc agent string.
    :config generic config for this application.
    """
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    config: util.Config = util.Config.load_config("configuration.yaml")
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
        try:
            service.creation_flags = subprocess.CREATE_NO_WINDOW
        except AttributeError:
            pass
        driver = webdriver.Chrome(service=service, options=options)
        atexit.register(driver.quit)
        return driver

    else:
        logger.info("Starting browser in development mode")
        if config.mode == "SERVER":
            driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
        else:
            driver = webdriver.Chrome(options=options)
        atexit.register(driver.quit)
        return driver


def init_browser(*, headless: bool, agent: str, execution_mode: str) -> WebDriver:
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
    logger.info(f"Starting browser in {execution_mode}")
    driver: WebDriver | None = None

    options = Options()
    options.add_argument("user-agent=" + agent)
    options.add_argument("log-level=3")
    if headless:
        options.add_argument("--headless")

    if execution_mode == "DOCKER":  # This is linux installation
        options.add_argument("--no-sandbox")  # causes chrome to crash in screen-less environment
        options.add_argument("--disable-dev-shm-usage")  # causes chrome to crash in screen-less environment
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options, chrome_options=options)

    if execution_mode == "DEV_LINUX":  # This is linux installation
        driver = webdriver.Chrome(options=options)

    if execution_mode == "DEV_WINDOWS":  # This is Windows Installation
        driver = webdriver.Chrome(options=options)

    if execution_mode == "DIST_WINDOWS":  # This is Windows installation, but for distribution.
        options.binary_location = "bin/chrome/chrome.exe"
        options.add_argument("--log-level=OFF")
        args = ["hide_console", ]
        service = Service("bin/chromedriver.exe", service_args=args)
        try:
            service.creation_flags = subprocess.CREATE_NO_WINDOW
        except AttributeError:
            pass
        driver = webdriver.Chrome(service=service, options=options)

    if driver is None:
        logger.critical("Unable to initialize browser. Error unknown.")
        raise Exception("Unknown error")

    atexit.register(driver.quit)
    return driver
