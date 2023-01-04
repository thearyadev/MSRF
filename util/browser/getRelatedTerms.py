import logging

import requests


def getRelatedTerms(word: str, pc_user_agent: str) -> list[str]:
    logger: logging.Logger = logging.getLogger("msrf")

    try:
        r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers={'User-agent': pc_user_agent})
        return r.json()[1]
    except Exception as e:
        logger.critical(f"Unable to get related search terms. {e}")
        return []
