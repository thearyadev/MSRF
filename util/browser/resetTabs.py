from selenium.webdriver.chrome.webdriver import WebDriver
import time


def resetTabs(browser: WebDriver, BASE_URL: str):
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
    except:
        browser.get(BASE_URL)
