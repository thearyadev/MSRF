import ipapi


def get_c_code_lang_and_offset() -> tuple:
    try:
        nfo = ipapi.location()
        lang = nfo['languages'].split(',')[0]
        geo = nfo['country']
        tz = str(round(int(nfo['utc_offset']) / 100 * 60))
        return lang, geo, tz
    except Exception as e:
        print(e)
        return 'en-CA', 'CA', '-300'
