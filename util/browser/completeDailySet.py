import util
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
import urllib.parse


def completeDailySet(browser: WebDriver, base_url: str):
    d = util.getDashboardData(browser)['dailySetPromotions']
    todayDate = datetime.today().strftime('%m/%d/%Y')
    todayPack = []
    for date, data in d.items():
        if date == todayDate:
            todayPack = data
    for activity in todayPack:
        try:
            if activity['complete'] == False:
                cardNumber = int(activity['offerId'][-1:])
                if activity['promotionType'] == "urlreward":
                    print('[DAILY SET]', 'Completing search of card ' + str(cardNumber))
                    util.completeDailySetSearch(browser, cardNumber)
                if activity['promotionType'] == "quiz":
                    if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                        print('[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                        util.completeDailySetThisOrThat(browser, cardNumber, base_url=base_url)
                    elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity[
                        'pointProgress'] == 0:
                        print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                        util.completeDailySetQuiz(browser, cardNumber, base_url=base_url)
                    elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                        searchUrl = urllib.parse.unquote(
                            urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                        searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for filter in searchUrlQueries['filters'][0].split(" "):
                            filter = filter.split(':', 1)
                            filters[filter[0]] = filter[1]
                        if "PollScenarioId" in filters:
                            print('[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                            util.completeDailySetSurvey(browser, cardNumber)
                        else:
                            print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                            util.completeDailySetVariableActivity(browser, cardNumber)
        except:
            util.resetTabs(browser, base_url)
