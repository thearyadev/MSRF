import json
import logging

import requests
from datetime import date, timedelta


def getGoogleTrends(numberOfwords: int, LANG: str, GEO: str) -> list:
    """
    Gets a list of search terms from Google Trends following the area and language defined.

    """

    logger: logging.Logger = logging.getLogger("msrf")  # get logger
    logger.info("Getting search terms")
    search_terms = []
    i = 0
    while len(search_terms) < numberOfwords:
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + LANG + '&ed=' + str(
            (date.today() - timedelta(days=i)).strftime('%Y%m%d')) + '&geo=' + GEO + '&ns=15')
        google_trends = json.loads(r.text[6:])
        for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            search_terms.append(topic['title']['query'].lower())
            for related_topic in topic['relatedQueries']:
                search_terms.append(related_topic['query'].lower())
        search_terms = list(set(search_terms))
    del search_terms[numberOfwords:(len(search_terms) + 1)]
    return search_terms
