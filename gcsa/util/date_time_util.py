from datetime import datetime, date
from dateutil.tz import gettz
from tzlocal import get_localzone_name


def ensure_localisation(dt, timezone=get_localzone_name()):
    """Insures localisation with provided timezone on "datetime" object.

    Does nothing to object of type "date"."""

    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            tz = gettz(timezone)
            dt = dt.replace(tzinfo=tz)
        return dt
    elif isinstance(dt, date):
        return dt
    else:
        raise TypeError('"date" or "datetime" object expected, not {!r}.'.format(dt.__class__.__name__))
