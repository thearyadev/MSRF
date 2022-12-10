from types import SimpleNamespace

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


def browser_setup(*, headless_mode: bool, user_agent: str, config: SimpleNamespace) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument('lang=' + config.LANG.split("-")[0])
    if headless_mode:
        options.add_argument("--headless")
    options.add_argument('log-level=3')
    chrome_browser_obj = webdriver.Chrome(options=options)
    return chrome_browser_obj
