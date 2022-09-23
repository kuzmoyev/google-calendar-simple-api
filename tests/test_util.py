from unittest import TestCase

from beautiful_date import Sept

from gcsa.util.date_time_util import ensure_localisation


class TestReminder(TestCase):
    def test_ensure_localisation(self):
        initial_date = 23 / Sept / 2022
        d = ensure_localisation(initial_date)
        # Shouldn't do anything to date
        self.assertEqual(initial_date, d)

        initial_date_time = initial_date[:]
        self.assertIsNone(initial_date_time.tzinfo)
        dt_with_tz = ensure_localisation(initial_date_time)
        self.assertIsNotNone(dt_with_tz.tzinfo)
        self.assertNotEqual(dt_with_tz, initial_date_time)

        dt_with_tz_unchanged = ensure_localisation(dt_with_tz)
        self.assertEqual(dt_with_tz, dt_with_tz_unchanged)

        with self.assertRaises(TypeError):
            ensure_localisation('Hello')
