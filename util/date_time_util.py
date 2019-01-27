from datetime import datetime, timedelta, date

import pytz
from tzlocal import get_localzone


def get_utc_datetime(dt, *args, **kwargs):
    if isinstance(dt, datetime):
        return dt.isoformat()
    else:
        return datetime(dt, *args, **kwargs).isoformat()


def date_range(start_date, day_count):
    for n in range(day_count):
        yield start_date + timedelta(n)


def insure_localisation(dt, timezone=str(get_localzone())):
    """Insures localisation with provided timezone on "datetime" object.

    Does nothing to object of type "date"."""

    if isinstance(dt, datetime):
        tz = pytz.timezone(timezone)
        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt
    elif isinstance(dt, date):
        return dt
    else:
        raise TypeError('"date" or "datetime" object expected, not {!r}.'.format(dt.__class__.__name__))
