import util

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time


def completePunchCards(browser: WebDriver, BASE_URL: str):
    punchCards = util.getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        try:
            if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0:
                if BASE_URL == "https://rewards.microsoft.com":
                    util.completePunchCard(browser, punchCard['parentPromotion']['attributes']['destination'], punchCard['childPromotions'])
                else:
                    url = punchCard['parentPromotion']['attributes']['destination']
                    path = url.replace(
                        'https://account.microsoft.com/rewards/dashboard/', '')
                    userCode = path[:4]
                    dest = 'https://account.microsoft.com/rewards/dashboard/' + \
                        userCode + path.split(userCode)[1]
                    util.completePunchCard(browser, url, punchCard['childPromotions'])
        except:
            util.resetTabs(browser, BASE_URL=BASE_URL)
    time.sleep(2)
    browser.get(BASE_URL)
    time.sleep(2)
