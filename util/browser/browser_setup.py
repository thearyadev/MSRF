from types import SimpleNamespace

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from deprecated import deprecated
from selenium.webdriver.chrome.options import Options

import util


@deprecated(reason="new version of this method has been created.", version="beta")
def browser_setup(*, headless_mode: bool, user_agent: str, config: SimpleNamespace) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("user-agent=" + user_agent)
    if headless_mode:
        options.add_argument("--headless")
    options.add_argument('log-level=3')
    chrome_browser_obj = webdriver.Chrome(options=options)
    return chrome_browser_obj


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
