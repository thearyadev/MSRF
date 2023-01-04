import custom_logging
import util
from selenium.webdriver.chrome.webdriver import WebDriver
import logging
from util import deprecated


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
