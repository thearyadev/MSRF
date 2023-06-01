import requests

import custom_logging


def getRelatedTerms(word: str, pc_user_agent: str) -> list[str]:
    logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(
        console=True, colors=True
    )
    try:
        r = requests.get(
            "https://api.bing.com/osjson.aspx?query=" + word,
            headers={"User-agent": pc_user_agent},
        )
        return r.json()[1]
    except Exception as e:
        logger.critical(f"Unable to get related search terms. {e}")
        return []
