import time

from selenium.webdriver.common.by import By

import util
from types import SimpleNamespace
from rich import print
from selenium.webdriver.chrome.webdriver import WebDriver

config: SimpleNamespace = util.load_config("configuration.yaml")
logger: util.ConsoleLogger = util.ConsoleLogger()

logger.log("Loaded ./configuration.yaml")
logger.log(f"Accounts Detected: {len(config.MicrosoftAccounts)}")


def main():
    # main loop

    for account in config.MicrosoftAccounts:
        POINTS = 0
        # init browser
        logger.log(f"Current Account: {account}")
        browser: WebDriver = util.browser_setup(headless_mode=True, user_agent=config.pc_user_agent, config=config)
        logger.log("Attempting login...")
        # go through login process
        util.login(browser, account.email, account.password, logger=logger, isMobile=False)
        logger.log("Login successful")
        browser.get('https://account.microsoft.com/')
        util.waitUntilVisible(browser, By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a', 20)

        if browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').get_attribute(
                'target') == '_blank':
            BASE_URL = 'https://rewards.microsoft.com'
            browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').click()
            time.sleep(1)
            browser.switch_to.window(window_name=browser.window_handles[0])
            browser.close()
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(10)
        else:
            BASE_URL = 'https://account.microsoft.com/rewards'
            browser.get(BASE_URL)
        POINTS = util.getPointCount(browser, BASE_URL)
        logger.log(f"Current Points: {POINTS}")
        logger.log("Setup complete. Starting point farmer.")
        logger.log("Attempting to complete 'Daily Set'")
        util.completeDailySet(browser, base_url=BASE_URL)
        logger.log("Successfully completed 'Daily Set'")
        logger.log("Attempting to complete 'Punch Cards'")
        util.completePunchCards(browser, BASE_URL=BASE_URL)
        logger.log("Successfully completed 'Punch Cards'")
        logger.log("Attempting to complete 'Additional Promotions'")
        util.completeMorePromotions(browser, BASE_URL=BASE_URL)
        logger.log("Successfully completed 'Additional Promotions'")
        POINTS = util.getPointCount(browser, BASE_URL)
        remainingSearches, remainingSearchesM = util.getRemainingSearches(browser)
        if remainingSearches != 0:
            logger.log("Searches available. Executing searches...")
            util.bingSearches(browser,
                              remainingSearches,
                              px=POINTS,
                              logger=logger,
                              LANG=config.LANG,
                              GEO=config.GEO,
                              agent=config.pc_user_agent)
            logger.log("Successfully completed all PC searches")
        browser.quit()
        if remainingSearchesM != 0:
            browser = util.browser_setup(headless_mode=True, user_agent=config.mobile_user_agent, config=config)
            logger.log("Logging in for mobile searches...")
            util.login(browser, account['username'], account['password'], logger=logger, isMobile=True)
            logger.log("Mobile login successful.")
            logger.log("Searches Available. Executing mobile searches...")

            util.bingSearches(browser,
                              remainingSearchesM,
                              px=POINTS,
                              logger=logger,
                              LANG=config.LANG,
                              GEO=config.GEO,
                              agent=config.mobile_user_agent,
                              isMobile=True)
            logger.log("Successfully completed all PC searches")
            browser.quit()

        if remainingSearchesM == 0 and remainingSearches == 0:
            logger.log("No searches available. Skipping...")

        try:
            POINTS = util.getPointCount(browser, BASE_URL)
            logger.log(F"Closing Point Total: {POINTS}")
        except Exception:
            pass

if __name__ == "__main__":
    main()
