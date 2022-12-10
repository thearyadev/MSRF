import util
from selenium.webdriver.chrome.webdriver import WebDriver

def completeMorePromotions(browser: WebDriver, BASE_URL: str):
    morePromotions = util.getDashboardData(browser)['morePromotions']
    i = 0
    for promotion in morePromotions:
        try:
            i += 1
            if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                if promotion['promotionType'] == "urlreward":
                    util.completeMorePromotionSearch(browser, i)
                elif promotion['promotionType'] == "quiz" and promotion['pointProgress'] == 0:
                    if promotion['pointProgressMax'] == 10:
                        util.completeMorePromotionABC(browser, i)
                    elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                        util.completeMorePromotionQuiz(browser, i, BASE_URL=BASE_URL)
                    elif promotion['pointProgressMax'] == 50:
                        util.completeMorePromotionThisOrThat(browser, i, BASE_URL=BASE_URL)
                else:
                    if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                        util.completeMorePromotionSearch(browser, i)
        except:
            util.resetTabs(browser, BASE_URL=BASE_URL)