import util
from selenium.webdriver.chrome.webdriver import WebDriver
import logging


def bingSearches(browser: WebDriver,
                 numberOfSearches: int,
                 px: int,
                 LANG: str,
                 GEO: str,
                 agent: str,
                 isMobile: bool = False):
    logger: logging.Logger = logging.getLogger("msrf")

    i = 0
    search_terms = util.getGoogleTrends(numberOfSearches, LANG=LANG, GEO=GEO)
    for word in search_terms:
        i += 1
        logger.info(f"Searching... {str(i)} / {str(numberOfSearches)}")
        points = util.bingSearch(browser, word, isMobile)
        if points <= px:
            relatedTerms = util.getRelatedTerms(word, pc_user_agent=agent)
            for term in relatedTerms :
                points = util.bingSearch(browser, term, isMobile)
                if not points <= px :
                    break
        if points > 0:
            px = points
        else:
            break