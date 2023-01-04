import custom_logging
import util
from selenium.webdriver.chrome.webdriver import WebDriver
import logging
from util import deprecated


@deprecated
def bing_searches(browser: WebDriver,
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
            for term in relatedTerms:
                points = util.bingSearch(browser, term, isMobile)
                if not points <= px:
                    break
        if points > 0:
            px = points
        else:
            break


def exec_bing_searches(*, browser: WebDriver,
                       searchCount: int,
                       terms: list[str],
                       starting_points: int,
                       mobile: bool,
                       agent: str):
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)

    for i, searchTerm in enumerate(terms):
        logger.info(f"Executing search # {i + 1}/{searchCount}")
        points = util.bingSearch(browser, searchTerm, mobile)
        if points <= starting_points:
            relatedTerms = util.getRelatedTerms(searchTerm, agent)
            for relatedSearchTerm in relatedTerms:
                points = util.bingSearch(browser, relatedSearchTerm, mobile)
                if not points <= starting_points:
                    break
            if points > 0:
                starting_points = points
            else:
                break

