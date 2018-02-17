from datetime import datetime, date

from tzlocal import get_localzone

from util.date_time_util import insure_localisation


class Duration:
    """Represents properties that contain a duration of time."""

    def __init__(self, w=None, d=None, h=None, m=None, s=None):
        """
        :param w: weeks
        :param d: days
        :param h: hours
        :param m: minutes
        :param s: seconds
        """

        self.w = w
        self.d = d
        self.h = h
        self.m = m
        self.s = s

    def __str__(self):
        res = 'P'
        if self.w:
            res += '{}W'.format(self.w)
        if self.d:
            res += '{}D'.format(self.d)
        if self.h or self.m or self.s:
            res += 'T'
        if self.h:
            res += '{}H'.format(self.h)
        if self.m:
            res += '{}M'.format(self.m)
        if self.s:
            res += '{}S'.format(self.s)

        return res


class _DayOfTheWeek:
    _short = None

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return str(self.n) + self._short


class _DayOfTheWeekMeta(type):
    _short = None

    def __str__(self):
        return self._short


class SUNDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'SU'


class MONDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'MO'


class TUESDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'TU'


class WEDNESDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'WE'


class THURSDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'TH'


class FRIDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'FR'


class SATURDAY(_DayOfTheWeek, metaclass=_DayOfTheWeekMeta):
    _short = 'SA'


DEFAULT_WEEK_START = SUNDAY

HOURLY = 'HOURLY'
MINUTELY = 'MINUTELY'

DAILY = 'DAILY'
WEEKLY = 'WEEKLY'
MONTHLY = 'MONTHLY'
YEARLY = 'YEARLY'


class Recurrence:
    @staticmethod
    def times(dts, timezone=str(get_localzone())):
        """Converts datetime(s) set to RDATE format.

        :param dts: datetime object or list of datetime objects
        :param timezone: Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                         the computers configured local timezone(if any) is used.
        :return: RDATE string of datetimes with specified timezone.
        """

        if not isinstance(dts, list):
            dts = [dts]

        localized_datetimes = []
        for dt in dts:
            if not (isinstance(dt, date) or isinstance(dt, datetime)):
                msg = 'The datetimes object(s) must be datetime, not {!r}.'.format(dt.__class__.__name__)
                raise TypeError(msg)
            localized_datetimes.append(insure_localisation(dt, timezone))

        return 'RDATE;TZID={}:{}'.format(timezone, ','.join(d.strftime('%Y%m%dT%H%M%S') for d in localized_datetimes))

    @staticmethod
    def dates(ds):
        """Converts date(s) set to RDATE format.

        :param ds: date/datetime object or list of date/datetime objects
        :return: RDATE string of dates.
        """
        if not isinstance(ds, list):
            ds = [ds]

        for d in ds:
            if not (isinstance(d, (date, datetime))):
                msg = 'The dates object(s) must be date or datetime, not {!r}.'.format(d.__class__.__name__)
                raise TypeError(msg)

        return 'RDATE;VALUE=DATE:' + ','.join(d.strftime('%Y%m%d') for d in ds)

    @staticmethod
    def period(ps, timezone=str(get_localzone())):
        """Converts date period(s) to RDATE format.

        Period is defined as tuple of starting date/datetime and ending date/datetime or duration as Duration object.

        :param ps: period or list of periods.
        :param timezone: Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                         the computers configured local timezone(if any) is used.
        :return: RDATE string of periods.
        """
        if not isinstance(ps, list):
            ps = [ps]

        period_strings = []
        for start, end in ps:
            if not isinstance(start, (date, datetime)):
                msg = 'The start object(s) must be a date or datetime, not {!r}.'.format(end.__class__.__name__)
                raise TypeError(msg)

            start = insure_localisation(start, timezone)
            if isinstance(end, (date, datetime)):
                end = insure_localisation(end, timezone)
                pstr = '{}/{}'.format(start.strftime('%Y%m%dT%H%M%S'), end.format(start.strftime('%Y%m%dT%H%M%S')))
            elif isinstance(end, Duration):
                pstr = '{}/{}'.format(start.strftime('%Y%m%dT%H%M%S'), end)
            else:
                msg = 'The end object(s) must be a date, datetime or Duration, not {!r}.'.format(end.__class__.__name__)
                raise TypeError(msg)
            period_strings.append(pstr)

        return 'RDATE;VALUE=PERIOD:' + ','.join(period_strings)

    @staticmethod
    def rule(freq=DAILY,
             interval=None,
             count=None,
             by_minute=None,  # BYMINUTE
             by_hour=None,  # BYHOUR
             by_week_day=None,  # BYDAY
             by_month_day=None,  # BYMONTHDAY
             by_year_day=None,  # BYYEARDAY
             by_week=None,  # BYWEEKNO
             by_month=None,  # BYMONTH
             by_set_pos=None,  # BYSETPOS
             week_start=DEFAULT_WEEK_START  # WKST
             ):
        """This property defines a rule or repeating pattern for recurring events."""
        """If none of the by_day, by_month_day, or by_year_day are specified, the day is gotten from start date."""
        pass
