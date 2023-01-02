from types import SimpleNamespace

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from deprecated import deprecated
from selenium.webdriver.chrome.options import Options

import util





def init_browser(*, headless: bool, agent: str) -> WebDriver:
    """
    Initializes a new Chrome instance using Selenium and chromedriver.

    :headless browser operation mode. Headless will not display a window.
    :agent mobile or pc agent string.
    :config generic config for this application.
    """

    options = Options()
    options.add_argument("user-agent=" + agent)
    if headless:
        options.add_argument("--headless")
    options.add_argument("log-level=3")
    return webdriver.Chrome(options=options)
