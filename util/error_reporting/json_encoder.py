import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    """I stole this code from stackoverflow. It's an encoder that supports encoding Dict Keys for the json module."""

    def _preprocess_date(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.timedelta)):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {
                self._preprocess_date(k): self._preprocess_date(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [self._preprocess_date(i) for i in obj]
        return obj

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.timedelta)):
            return obj.isoformat()
        return super().default(obj)

    def iterencode(self, obj, **kwargs):
        return super().iterencode(self._preprocess_date(obj))
