from unittest import TestCase

from gcsa.recurrence import Recurrence, \
    SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY, \
    MO, TU, WE, TH, FR, SA, SU


class TestRecurrence(TestCase):
    def assert_rrule_equal(self, first, second, msg=None):
        first_set = set(first.split(';'))
        second_set = set(second.split(';'))
        self.assertSetEqual(first_set, second_set, msg)

    def test__rule(self):
        r = Recurrence._rule
        self.assert_rrule_equal(r(), 'FREQ=DAILY;WKST=SU')
        self.assert_rrule_equal(r(freq=WEEKLY), 'FREQ=WEEKLY;WKST=SU')
        self.assert_rrule_equal(r(count=5), 'FREQ=DAILY;COUNT=5;WKST=SU')
        self.assert_rrule_equal(r(by_second=13), 'FREQ=DAILY;BYSECOND=13;WKST=SU')
        self.assert_rrule_equal(r(by_minute=44), 'FREQ=DAILY;BYMINUTE=44;WKST=SU')
        self.assert_rrule_equal(r(by_hour=22), 'FREQ=DAILY;BYHOUR=22;WKST=SU')
        self.assert_rrule_equal(r(by_week_day=WE), 'FREQ=DAILY;BYDAY=WE;WKST=SU')
        self.assert_rrule_equal(r(by_week_day=TH(-1)), 'FREQ=DAILY;BYDAY=-1TH;WKST=SU')
        self.assert_rrule_equal(r(by_month_day=30), 'FREQ=DAILY;BYMONTHDAY=30;WKST=SU')
        self.assert_rrule_equal(r(by_year_day=48), 'FREQ=DAILY;BYYEARDAY=48;WKST=SU')
        self.assert_rrule_equal(r(by_week=-51), 'FREQ=DAILY;BYWEEKNO=-51;WKST=SU')
        self.assert_rrule_equal(r(by_month=4), 'FREQ=DAILY;BYMONTH=4;WKST=SU')
        self.assert_rrule_equal(r(by_set_pos=4, by_month=3), 'FREQ=DAILY;BYSETPOS=4;BYMONTH=3;WKST=SU')
        self.assert_rrule_equal(r(week_start=MO), 'FREQ=DAILY;WKST=MO')
