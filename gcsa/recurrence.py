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


class _DayOfTheWeekMeta(type):
    """ Metaclass used for weekdays classes to override __str__ method of the class (not the instances),
        so the weekday class' __str__ method returns corresponding weekday short form.

        >>> str(SU)
        'SU'

        >>> str(FR)
        'FR'
    """
    _short = None

    def __str__(self):
        return self._short


class _DayOfTheWeek(metaclass=_DayOfTheWeekMeta):
    _short = None

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return str(self.n) + self._short


class SUNDAY(_DayOfTheWeek):
    _short = 'SU'


class MONDAY(_DayOfTheWeek):
    _short = 'MO'


class TUESDAY(_DayOfTheWeek):
    _short = 'TU'


class WEDNESDAY(_DayOfTheWeek):
    _short = 'WE'


class THURSDAY(_DayOfTheWeek):
    _short = 'TH'


class FRIDAY(_DayOfTheWeek):
    _short = 'FR'


class SATURDAY(_DayOfTheWeek):
    _short = 'SA'


SU = SUNDAY
MO = MONDAY
TU = TUESDAY
WE = WEDNESDAY
TH = THURSDAY
FR = FRIDAY
SA = SATURDAY

DEFAULT_WEEK_START = SUNDAY

SECONDLY = 'SECONDLY'
MINUTELY = 'MINUTELY'
HOURLY = 'HOURLY'

DAILY = 'DAILY'
WEEKLY = 'WEEKLY'
MONTHLY = 'MONTHLY'
YEARLY = 'YEARLY'


class Recurrence:

    @staticmethod
    def rule(
            freq=DAILY,
            interval=None,
            count=None,
            by_second=None,
            by_minute=None,
            by_hour=None,
            by_week_day=None,
            by_month_day=None,
            by_year_day=None,
            by_week=None,
            by_month=None,
            by_set_pos=None,
            week_start=DEFAULT_WEEK_START
    ):
        """This property defines a rule or repeating pattern for recurring events.

        :param freq:
                identifies the type of recurrence rule. Possible values are HOURLY,
                MINUTELY, DAILY, WEEKLY, MONTHLY, YEARLY. Default: DAILY
        :param interval:
                positive integer representing how often the recurrence rule repeats
        :param count:
                number of occurrences at which to range-bound the recurrence
        :param by_second:
                second or list of seconds within a minute. Valid values are 0 to 60
        :param by_minute:
                minute or list of minutes within a hour. Valid values are 0 to 59
        :param by_hour:
                hour or list of hours of the day. Valid values are 0 to 23
        :param by_week_day:
                day or list of days of the week.
                Possible values: :py:class:~SUNDAY, :py:class:~MONDAY, :py:class:~TUESDAY, :py:class:~WEDNESDAY,
                :py:class:~THURSDAY ,:py:class:~FRIDAY, :py:class:~SATURDAY
        :param by_month_day:
                day or list of days of the month. Valid values are 1 to 31 or -31 to -1.
                For example, -10 represents the tenth to the last day of the month.
        :param by_year_day:
                day or list of days of the year. Valid values are 1 to 366 or -366 to -1.
                For example, -1 represents the last day of the year.
        :param by_week:
                ordinal or list of ordinals specifying weeks of the year. Valid values are 1 to 53 or -53 to -1.
        :param by_month:
                month or list of months of the year. Valid values are 1 to 12.
        :param by_set_pos:
                value or list of values which corresponds to the nth occurrence within the set of events
                specified by the rule. Valid values are 1 to 366 or -366 to -1.
                It can only be used in conjunction with another by_xxx parameter.
        :param week_start:
                the day on which the workweek starts.
                Possible values: :py:class:~SUNDAY, :py:class:~MONDAY, :py:class:~TUESDAY, :py:class:~WEDNESDAY,
                :py:class:~THURSDAY ,:py:class:~FRIDAY, :py:class:~SATURDAY

        :return:
                string representing specified recurrence rule in `RRULE format`_.

        .. note:: If none of the by_day, by_month_day, or by_year_day are specified, the day is gotten from start date.


        .. _`RRULE format`: https://tools.ietf.org/html/rfc5545#section-3.8.5
        """
        return 'RRULE:' + Recurrence._rule(freq, interval, count, by_second, by_minute, by_hour, by_week_day,
                                           by_month_day, by_year_day, by_week, by_month, by_set_pos, week_start)

    @staticmethod
    def exclude_rule(
            freq=DAILY,
            interval=None,
            count=None,
            by_second=None,
            by_minute=None,
            by_hour=None,
            by_week_day=None,
            by_month_day=None,
            by_year_day=None,
            by_week=None,
            by_month=None,
            by_set_pos=None,
            week_start=DEFAULT_WEEK_START
    ):
        """This property defines an exclusion rule or repeating pattern for recurring events.

        :param freq:
                identifies the type of recurrence rule. Possible values are HOURLY,
                MINUTELY, DAILY, WEEKLY, MONTHLY, YEARLY. Default: DAILY
        :param interval:
                positive integer representing how often the recurrence rule repeats
        :param count:
                number of occurrences at which to range-bound the recurrence
        :param by_second:
                second or list of seconds within a minute. Valid values are 0 to 60
        :param by_minute:
                minute or list of minutes within a hour. Valid values are 0 to 59
        :param by_hour:
                hour or list of hours of the day. Valid values are 0 to 23
        :param by_week_day:
                day or list of days of the week.
                Possible values: :py:class:~SUNDAY, :py:class:~MONDAY, :py:class:~TUESDAY, :py:class:~WEDNESDAY,
                :py:class:~THURSDAY ,:py:class:~FRIDAY, :py:class:~SATURDAY
        :param by_month_day:
                day or list of days of the month. Valid values are 1 to 31 or -31 to -1.
                For example, -10 represents the tenth to the last day of the month.
        :param by_year_day:
                day or list of days of the year. Valid values are 1 to 366 or -366 to -1.
                For example, -1 represents the last day of the year.
        :param by_week:
                ordinal or list of ordinals specifying weeks of the year. Valid values are 1 to 53 or -53 to -1.
        :param by_month:
                month or list of months of the year. Valid values are 1 to 12.
        :param by_set_pos:
                value or list of values which corresponds to the nth occurrence within the set of events
                specified by the rule. Valid values are 1 to 366 or -366 to -1.
                It can only be used in conjunction with another by_xxx parameter.
        :param week_start:
                the day on which the workweek starts.
                Possible values: :py:class:~SUNDAY, :py:class:~MONDAY, :py:class:~TUESDAY, :py:class:~WEDNESDAY,
                :py:class:~THURSDAY ,:py:class:~FRIDAY, :py:class:~SATURDAY

        :return:
                string representing specified recurrence rule in `RRULE format`_.

        .. note:: If none of the by_day, by_month_day, or by_year_day are specified, the day is gotten from start date.


        .. _`RRULE format`: https://tools.ietf.org/html/rfc5545#section-3.8.5
        """
        return 'EXRULE:' + Recurrence._rule(freq, interval, count, by_second, by_minute, by_hour, by_week_day,
                                            by_month_day, by_year_day, by_week, by_month, by_set_pos, week_start)

    @staticmethod
    def dates(ds):
        """Converts date(s) set to RDATE format.

        :param ds: date/datetime object or list of date/datetime objects
        :return: RDATE string of dates.
        """
        return 'RDATE;' + Recurrence._dates(ds)

    @staticmethod
    def times(dts, timezone=str(get_localzone())):
        """Converts datetime(s) set to RDATE format.

        :param dts: datetime object or list of datetime objects
        :param timezone: Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                         the computers configured local timezone(if any) is used.
        :return: RDATE string of datetimes with specified timezone.
        """
        return 'RDATE;' + Recurrence._times(dts, timezone)

    @staticmethod
    def periods(ps, timezone=str(get_localzone())):
        """Converts date period(s) to RDATE format.

        Period is defined as tuple of starting date/datetime and ending date/datetime or duration as Duration object:
            (date/datetime, date/datetime/Duration)

        :param ps: period or list of periods.
        :param timezone: Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                         the computers configured local timezone(if any) is used.
        :return: RDATE string of periods.
        """
        return 'RDATE;' + Recurrence._periods(ps, timezone)

    @staticmethod
    def exclude_dates(ds):
        """Converts date(s) set to EXDATE format.

        :param ds: date/datetime object or list of date/datetime objects
        :return: EXDATE string of dates.
        """
        return 'EXDATE;' + Recurrence._dates(ds)

    @staticmethod
    def exclude_times(dts, timezone=str(get_localzone())):
        """Converts datetime(s) set to EXDATE format.

        :param dts: datetime object or list of datetime objects
        :param timezone: Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                         the computers configured local timezone(if any) is used.
        :return: EXDATE string of datetimes with specified timezone.
        """
        return 'EXDATE;' + Recurrence._times(dts, timezone)

    @staticmethod
    def exclude_periods(ps, timezone=str(get_localzone())):
        """Converts date period(s) to EXDATE format.

        Period is defined as tuple of starting date/datetime and ending date/datetime or duration as Duration object:
            (date/datetime, date/datetime/Duration)

        :param ps: period or list of periods.
        :param timezone: Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                         the computers configured local timezone(if any) is used.
        :return: EXDATE string of periods.
        """
        return 'EXDATE;' + Recurrence._periods(ps, timezone)

    @staticmethod
    def _times(dts, timezone=str(get_localzone())):
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

        return 'TZID={}:{}'.format(timezone, ','.join(d.strftime('%Y%m%dT%H%M%S') for d in localized_datetimes))

    @staticmethod
    def _dates(ds):
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

        return 'VALUE=DATE:' + ','.join(d.strftime('%Y%m%d') for d in ds)

    @staticmethod
    def _periods(ps, timezone=str(get_localzone())):
        """Converts date period(s) to RDATE format.

        Period is defined as tuple of starting date/datetime and ending date/datetime or duration as Duration object:
            (date/datetime, date/datetime/Duration)

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

        return 'VALUE=PERIOD:' + ','.join(period_strings)

    @staticmethod
    def _rule(
            freq=DAILY,
            interval=None,
            count=None,
            by_second=None,  # BYSECOND
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
        """This property defines a rule or repeating pattern for recurring events.

        :param freq:
                identifies the type of recurrence rule. Possible values are HOURLY,
                MINUTELY, DAILY, WEEKLY, MONTHLY, YEARLY. Default: DAILY
        :param interval:
                positive integer representing how often the recurrence rule repeats
        :param count:
                number of occurrences at which to range-bound the recurrence
        :param by_second:
                second or list of seconds within a minute. Valid values are 0 to 60
        :param by_minute:
                minute or list of minutes within a hour. Valid values are 0 to 59
        :param by_hour:
                hour or list of hours of the day. Valid values are 0 to 23
        :param by_week_day:
                day or list of days of the week.
                Possible values: :py:class:~SUNDAY, :py:class:~MONDAY, :py:class:~TUESDAY, :py:class:~WEDNESDAY,
                :py:class:~THURSDAY ,:py:class:~FRIDAY, :py:class:~SATURDAY
        :param by_month_day:
                day or list of days of the month. Valid values are 1 to 31 or -31 to -1.
                For example, -10 represents the tenth to the last day of the month.
        :param by_year_day:
                day or list of days of the year. Valid values are 1 to 366 or -366 to -1.
                For example, -1 represents the last day of the year.
        :param by_week:
                ordinal or list of ordinals specifying weeks of the year. Valid values are 1 to 53 or -53 to -1.
        :param by_month:
                month or list of months of the year. Valid values are 1 to 12.
        :param by_set_pos:
                value or list of values which corresponds to the nth occurrence within the set of events
                specified by the rule. Valid values are 1 to 366 or -366 to -1.
                It can only be used in conjunction with another by_xxx parameter.
        :param week_start:
                the day on which the workweek starts.
                Possible values: :py:class:~SUNDAY, :py:class:~MONDAY, :py:class:~TUESDAY, :py:class:~WEDNESDAY,
                :py:class:~THURSDAY ,:py:class:~FRIDAY, :py:class:~SATURDAY

        :return:
                string representing specified recurrence rule in `RRULE format`_.

        .. note:: If none of the by_day, by_month_day, or by_year_day are specified, the day is gotten from start date.


        .. _`RRULE format`: https://tools.ietf.org/html/rfc5545#section-3.8.5
        """

        def assure_iterable(it):
            return it if isinstance(it, (list, tuple, set)) else [it] if it else []

        def check_all_type_and_range(it, type_, range_, name, nonzero=False):
            low, high = range_
            if any(not isinstance(o, type_) or not (low <= o <= high) for o in it):
                raise ValueError('"{}" parameter must be a {} or list of {}s in range {}-{}.'
                                 .format(name, type_.__name__, type_.__name__, low, high))
            if nonzero and any(o == 0 for o in it):
                raise ValueError('"{}" parameter must be a {} or list of {}s in range {}-{} and nonzero.'
                                 .format(name, type_.__name__, type_.__name__, low, high))

        def check_all_type(it, type_, name):
            if any(not isinstance(o, type_) for o in it):
                raise ValueError('"{}" parameter must be a {} or list of {}s.'
                                 .format(name, type_.__name__, type_.__name__))

        def to_string(l):
            return ','.join(map(str, l)) if l else None

        if freq not in (HOURLY, MINUTELY, DAILY, WEEKLY, MONTHLY, YEARLY):
            raise ValueError('"freq" parameter must be one of HOURLY, MINUTELY, DAILY, WEEKLY, MONTHLY or YEARLY. '
                             '{} was provided'.format(freq))
        if interval and (isinstance(interval, int) or interval < 1):
            raise ValueError('"interval" parameter must be a positive int. '
                             '{} was provided'.format(interval))
        if count and (not isinstance(count, int) or count < 1):
            raise ValueError('"count" parameter must be a positive int. '
                             '{} was provided'.format(count))

        by_second = assure_iterable(by_second)
        check_all_type_and_range(by_second, int, (0, 60), "by_second")

        by_minute = assure_iterable(by_minute)
        check_all_type_and_range(by_minute, int, (0, 59), "by_minute")

        by_hour = assure_iterable(by_hour)
        check_all_type_and_range(by_hour, int, (0, 23), "by_hour")

        by_week_day = assure_iterable(by_week_day)
        check_all_type(by_week_day, (_DayOfTheWeek, _DayOfTheWeekMeta), "by_week_day")

        by_month_day = assure_iterable(by_month_day)
        check_all_type_and_range(by_month_day, int, (-31, 31), "by_month_day", nonzero=True)

        by_year_day = assure_iterable(by_year_day)
        check_all_type_and_range(by_year_day, int, (-366, 366), "by_year_day", nonzero=True)

        by_week = assure_iterable(by_week)
        check_all_type_and_range(by_week, int, (-53, 53), "by_week", nonzero=True)

        by_month = assure_iterable(by_month)
        check_all_type_and_range(by_month, int, (1, 12), "by_month")

        by_set_pos = assure_iterable(by_set_pos)
        check_all_type_and_range(by_set_pos, int, (-366, 366), "by_set_pos", nonzero=True)
        if by_set_pos and all(not v for v in (by_second, by_minute, by_hour,
                                              by_week_day, by_month_day, by_year_day,
                                              by_week, by_month)):
            raise ValueError('"by_set_pos" parameter can only be used in conjunction with another by_xxx parameter.')

        if not isinstance(week_start, (_DayOfTheWeek, _DayOfTheWeekMeta)):
            raise ValueError('"week_start" parameter must be one of SUNDAY, MONDAY, etc. '
                             '{} was provided'.format(week_start))

        rrule = 'FREQ={}'.format(freq)

        rule_properties = (
            ('INTERVAL', interval),
            ('COUNT', count),
            ('BYSECOND', to_string(by_second)),
            ('BYMINUTE', to_string(by_minute)),
            ('BYHOUR', to_string(by_hour)),
            ('BYDAY', to_string(by_week_day)),
            ('BYMONTHDAY', to_string(by_month_day)),
            ('BYYEARDAY', to_string(by_year_day)),
            ('BYWEEKNO', to_string(by_week)),
            ('BYMONTH', to_string(by_month)),
            ('BYSETPOS', to_string(by_set_pos)),
            ('WKST', week_start)
        )

        for key, value in rule_properties:
            if value:
                rrule += ';{}={}'.format(key, value)

        return rrule
