from datetime import datetime, date, time
from typing import overload, Union

from dateutil.tz import gettz
from tzlocal import get_localzone_name

from beautiful_date import BeautifulDate

DateOrDatetime = Union[date, datetime, BeautifulDate]


@overload
def ensure_localisation(dt: datetime, timezone: str = ...) -> datetime: ...


@overload
def ensure_localisation(dt: date, timezone: str = ...) -> date: ...


@overload
def ensure_localisation(dt: BeautifulDate, timezone: str = ...) -> BeautifulDate: ...


def ensure_localisation(dt: DateOrDatetime, timezone: str = get_localzone_name()) -> DateOrDatetime:
    """Ensures localisation with provided timezone on a datetime object.

    Does nothing to an object of type date."""
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            tz = gettz(timezone)
            dt = dt.replace(tzinfo=tz)
        return dt
    elif isinstance(dt, date):
        return dt
    else:
        raise TypeError('"date" or "datetime" object expected, not {!r}.'.format(dt.__class__.__name__))


def to_localized_iso(dt, timezone=get_localzone_name()):
    if not isinstance(dt, datetime):
        dt = datetime.combine(dt, time())
    return ensure_localisation(dt, timezone).isoformat()
