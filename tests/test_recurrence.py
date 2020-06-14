from functools import partial
from unittest import TestCase

from beautiful_date import Jun, Jul

from gcsa.recurrence import Recurrence, \
    WEEKLY, MO, WE, TH, Duration

r = Recurrence._rule
t = partial(Recurrence._times, timezone='Europe/Prague')
d = Recurrence._dates
p = Recurrence._periods


class TestRecurrence(TestCase):
    def assert_rrule_equal(self, first, second, msg=None):
        first_set = set(first.split(';'))
        second_set = set(second.split(';'))
        self.assertSetEqual(first_set, second_set, msg)

    def test__rule(self):
        self.assert_rrule_equal(r(), 'FREQ=DAILY;WKST=SU')
        self.assert_rrule_equal(r(freq=WEEKLY), 'FREQ=WEEKLY;WKST=SU')
        self.assert_rrule_equal(r(interval=2), 'FREQ=DAILY;INTERVAL=2;WKST=SU')
        self.assert_rrule_equal(r(count=5), 'FREQ=DAILY;COUNT=5;WKST=SU')
        self.assert_rrule_equal(r(until=14 / Jun / 2020), 'FREQ=DAILY;UNTIL=20200614T000000Z;WKST=SU')
        self.assert_rrule_equal(r(until=(14 / Jun / 2020)[15:49]), 'FREQ=DAILY;UNTIL=20200614T154900Z;WKST=SU')
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
        self.assert_rrule_equal(r(week_start=MO(4)), 'FREQ=DAILY;WKST=4MO')
        self.assert_rrule_equal(r(week_start=MO(-1)), 'FREQ=DAILY;WKST=-1MO')

    def test__rule_errors(self):
        def assert_value_error(**kwargs):
            with self.assertRaises(ValueError):
                r(**kwargs)

        def assert_type_error(**kwargs):
            with self.assertRaises(TypeError):
                r(**kwargs)

        assert_value_error(freq='MILLISECONDLY')  # MILLISECONDLY is not a valid frequency

        assert_value_error(interval=0)
        assert_value_error(interval=-4)

        assert_value_error(count=0)
        assert_value_error(count=-1)

        assert_type_error(until=15)

        assert_value_error(by_second=-1)
        assert_value_error(by_second=[4, -4, 5])
        assert_value_error(by_second=[4, 61, 5])

        assert_value_error(by_minute=-4)
        assert_value_error(by_minute=[4, -4, 5])
        assert_value_error(by_minute=[4, 60, 5])

        assert_value_error(by_hour=-4)
        assert_value_error(by_hour=[4, -4, 5])
        assert_value_error(by_hour=[4, 60, 5])

        assert_type_error(by_week_day=4)

        assert_value_error(by_month_day=0)
        assert_value_error(by_month_day=32)
        assert_value_error(by_month_day=-32)
        assert_value_error(by_month_day=[1, -32, 5])
        assert_value_error(by_month_day=[1, 0, 5])

        assert_value_error(by_year_day=0)
        assert_value_error(by_year_day=367)
        assert_value_error(by_year_day=-367)
        assert_value_error(by_year_day=[1, -367, 5])
        assert_value_error(by_year_day=[1, 0, 5])

        assert_value_error(by_week=0)
        assert_value_error(by_week=54)
        assert_value_error(by_week=-54)
        assert_value_error(by_week=[1, -54, 5])
        assert_value_error(by_week=[1, 0, 5])

        assert_value_error(by_month=0)
        assert_value_error(by_month=13)
        assert_value_error(by_month=-4)
        assert_value_error(by_month=[1, -1, 5])
        assert_value_error(by_month=[1, 0, 5])

        assert_value_error(week_start=3)

    def test__times(self):
        def assert_times_equal(dts, rtimes):
            self.assertEqual(t(dts), "TZID=Europe/Prague:" + rtimes)

        assert_times_equal((15 / Jun / 2020)[10:30],
                           "20200615T103000")
        assert_times_equal([(15 / Jun / 2020)[10:30]],
                           "20200615T103000")
        assert_times_equal([(15 / Jun / 2020)[10:30], (17 / Jul / 2020)[23:45]],
                           "20200615T103000,20200717T234500")
        assert_times_equal([(15 / Jun / 2020)[10:30], (17 / Jul / 2020)],
                           "20200615T103000,20200717T000000")

    def test__times_errors(self):
        with self.assertRaises(TypeError):
            t("hello")
        with self.assertRaises(TypeError):
            t([(15 / Jun / 2020)[10:30], "hello"])

    def test__dates(self):
        def assert_dates_equal(ds, rdates):
            self.assertEqual(d(ds), "VALUE=DATE:" + rdates)

        assert_dates_equal(15 / Jun / 2020,
                           "20200615")
        assert_dates_equal([(15 / Jun / 2020)],
                           "20200615")
        assert_dates_equal([15 / Jun / 2020, (17 / Jul / 2020)[23:45]],
                           "20200615,20200717")
        assert_dates_equal([(15 / Jun / 2020)[10:30], (17 / Jul / 2020)],
                           "20200615,20200717")

    def test__dates_errors(self):
        with self.assertRaises(TypeError):
            d("hello")
        with self.assertRaises(TypeError):
            d([15 / Jun / 2020, "hello"])

    def test__periods(self):
        def assert_periods_equal(ps, rperiods):
            self.assertEqual(p(ps), "VALUE=PERIOD:" + rperiods)

        assert_periods_equal(((15 / Jun / 2020), (17 / Jul / 2020)),
                             '20200615T000000Z/20200717T000000Z')
        assert_periods_equal(((15 / Jun / 2020), Duration(w=2, d=1)),
                             '20200615T000000Z/P2W1D')
        assert_periods_equal(((15 / Jun / 2020), Duration(w=2, d=1, m=10)),
                             '20200615T000000Z/P2W1DT10M')
        assert_periods_equal([((15 / Jun / 2020)[21:10], (17 / Jul / 2020)[22:12])],
                             '20200615T211000Z/20200717T221200Z')
        assert_periods_equal([((15 / Jun / 2020)[21:10], (17 / Jul / 2020)[22:12])],
                             '20200615T211000Z/20200717T221200Z')
        assert_periods_equal([((15 / Jun / 2020)[21:10], (17 / Jul / 2020)[22:12]),
                              ((15 / Jun / 2020)[21:10], Duration(w=2, d=1, m=10))],
                             '20200615T211000Z/20200717T221200Z,20200615T211000Z/P2W1DT10M')

    def test__periods_errors(self):
        with self.assertRaises(TypeError):
            p((15 / Jun / 2020, "hello"))
        with self.assertRaises(TypeError):
            p([("Hello", 15 / Jun / 2020)])
        with self.assertRaises(TypeError):
            p([(10 / Jun / 2020, 15 / Jun / 2020), ("Hello", 15 / Jun / 2020)])
