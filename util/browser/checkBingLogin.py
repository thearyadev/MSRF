import time
from selenium.webdriver.chrome.webdriver import WebDriver
import util
from selenium.webdriver.common.by import By


def checkBingLogin(browser: WebDriver, logger: util.ConsoleLogger,  isMobile: bool = False,) -> int:
    # Access Bing.com
    browser.get('https://bing.com/')
    # Wait 8 seconds
    time.sleep(8)
    # Accept Cookies
    try:
        browser.find_element(By.ID, 'bnp_btn_accept').click()
    except:
        pass
    if isMobile:
        try:
            time.sleep(1)
            browser.find_element(By.ID, 'mHamburger').click()
        except:
            try:
                browser.find_element(By.ID, 'bnp_btn_accept').click()
            except:
                pass
            try:
                browser.find_element(By.ID, 'bnp_ttc_close').click()
            except:
                pass
            time.sleep(1)
            try:
                browser.find_element(By.ID, 'mHamburger').click()
            except:
                pass
        try:
            time.sleep(1)
            browser.find_element(By.ID, 'HBSignIn').click()
        except:
            pass
        try:
            time.sleep(2)
            browser.find_element(By.ID, 'iShowSkip').click()
            time.sleep(3)
        except:
            if str(browser.current_url).split('?')[0] == "https://account.live.com/proofs/Add":
                input('Please complete the Security Check on ' + browser.current_url)
                exit()
    # Wait 2 seconds
    time.sleep(2)
    # Refresh page
    browser.get('https://bing.com/')
    # Wait 5 seconds
    time.sleep(10)
    # Update Counter
    try:
        if not isMobile:
            POINTS_COUNTER = int(browser.find_element(By.ID, 'id_rc').get_attribute('innerHTML'))
            return POINTS_COUNTER
        else:
            try:
                browser.find_element(By.ID, 'mHamburger').click()
            except:
                try:
                    browser.find_element(By.ID, 'bnp_btn_accept').click()
                except:
                    pass
                try:
                    browser.find_element(By.ID, 'bnp_ttc_close').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element(By.ID, 'mHamburger').click()
            time.sleep(1)
            POINTS_COUNTER = int(browser.find_element(By.ID, 'fly_id_rc').get_attribute('innerHTML'))
            return POINTS_COUNTER
    except:
        logger.log("Unable to validate login state... trying again. Username or password may be invalid.")
        checkBingLogin(browser, logger=logger, isMobile=isMobile)

