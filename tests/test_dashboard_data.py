import os
from datetime import datetime

import dotenv
import util
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
import atexit
import pytest_check as ptc

dotenv.load_dotenv()
config: util.Config = util.load_config("configuration.yaml")

x = 1


@pytest.fixture(scope="session")
def browser() -> WebDriver:
    browser = util.init_browser(headless=True, agent=config.pc_user_agent)
    util.authenticate_microsoft_account(
        browser=browser,
        account=util.MicrosoftAccount(
            email=os.getenv("MSRF_L2_TESTING_USERNAME"),
            password=os.getenv("MSRF_L2_TESTING_PASSWORD")
        )
    )
    browser.get("https://rewards.bing.com")
    atexit.register(browser.quit)
    return browser


@pytest.mark.trylast
class TestDashboardData:

    def test_dashboard_data_exists_on_page(self, browser: WebDriver):
        assert isinstance(browser.execute_script("return dashboard"), dict)

    def test_dashboard_data_model_conversion_no_exception(self, browser: WebDriver):
        util.load_dashboard_data(browser)

    def test_daily_set_data_is_valid(self, browser: WebDriver):
        accountData: util.DashboardData = util.load_dashboard_data(browser)
        ptc.is_not(accountData.dailySetPromotions, None)
        for promoDate, promoData in accountData.dailySetPromotions.items():
            promoDate: datetime.date
            promoData: list[util.DailyPromotion]
            for promo in promoData:
                ptc.is_not(promo.pointProgress, None)
                ptc.is_not(promo.pointProgressMax, None)
                ptc.assert_equal(bool(promo.promotionType), True)
                ptc.is_in(promo.promotionType, ('urlreward', 'quiz',))
                ptc.is_not(promo.complete, None)
                ptc.assert_equal(bool(promo.destinationUrl), True)

    def test_punch_cards_data_is_valid(self, browser: WebDriver):
        accountData: util.DashboardData = util.load_dashboard_data(browser)
        ptc.is_not(accountData.punchCards, None)
        for punchCard in accountData.punchCards:
            ptc.is_not(punchCard.parentPromotion, None)
            ptc.equal(bool(punchCard.parentPromotion.destinationUrl), True)
            ptc.equal(bool(punchCard.parentPromotion.destinationUrl), True)
            ptc.is_not(punchCard.parentPromotion.complete, None)
            ptc.is_not(punchCard.parentPromotion.pointProgressMax, None)
            ptc.is_not(punchCard.parentPromotion.pointProgress, None)

            if punchCard.childPromotion is not None:
                for childPromo in punchCard.childPromotion:
                    ptc.assert_equal(bool(childPromo.promotionType), True)
                    ptc.is_in(childPromo.promotionType, ('urlreward', 'quiz',))
                    ptc.is_not(childPromo.complete, None)
                    ptc.assert_equal(bool(childPromo.destinationUrl), True)
                    ptc.is_not(childPromo.pointProgressMax, None)
                    ptc.is_not(childPromo.pointProgress, None)

    def test_additional_promotions_data_is_valid(self, browser: WebDriver):
        accountData: util.DashboardData = util.load_dashboard_data(browser)
        ptc.is_not(accountData.morePromotions, None)
        for promo in accountData.morePromotions:
            ptc.is_not(promo.promotionType, None)
            ptc.is_in(promo.promotionType, ('urlreward', 'quiz', ''))
            ptc.is_not(promo.complete, None)
            ptc.is_not(promo.pointProgress, None)
            ptc.is_not(promo.pointProgressMax, None)
            ptc.assert_equal(bool(promo.destinationUrl), True)

    def test_user_data_is_valid(self, browser: WebDriver):
        accountData: util.DashboardData = util.load_dashboard_data(browser)
        ptc.is_not(accountData.userStatus, None)
        ptc.is_not(accountData.userStatus.availablePoints, None)
        ptc.is_not(accountData.userStatus.lifetimePoints, None)
        ptc.is_not(accountData.userStatus.lifetimePointsRedeemed, None)
        ptc.assert_equal(bool(accountData.userStatus.counters.pcSearch), True)
        ptc.assert_equal(bool(accountData.userStatus.counters.mobileSearch), True)
