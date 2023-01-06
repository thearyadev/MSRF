import time

from selenium.webdriver.chrome.webdriver import WebDriver


def resetTabs(browser: WebDriver, BASE_URL: str):
    """
    Closes all irrelevant tabs and returns to base_url
    """
    try:
        curr = browser.current_window_handle

        for handle in browser.window_handles:
            if handle != curr:
                browser.switch_to.window(handle)
                time.sleep(0.5)
                browser.close()
                time.sleep(0.5)

        browser.switch_to.window(curr)
        time.sleep(0.5)
        browser.get(BASE_URL)
    except Exception:
        browser.get(BASE_URL)
