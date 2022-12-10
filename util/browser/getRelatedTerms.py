import requests


def getRelatedTerms(word: str, pc_user_agent: str) -> list:
    try:
        r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers={'User-agent': pc_user_agent})
        return r.json()[1]
    except:
        return []
