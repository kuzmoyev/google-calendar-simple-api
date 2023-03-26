from datetime import timedelta

from beautiful_date import D, weeks

from gcsa.free_busy import FreeBusyQueryError
from gcsa.util.date_time_util import ensure_localisation
from tests.google_calendar_tests.mock_services.util import time_range_within
from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestFreeBusyService(TestCaseWithMockedService):
    def test_query_default(self):
        free_busy = self.gc.get_free_busy()

        time_min = ensure_localisation(D.now())
        time_max = time_min + 2 * weeks
        self.assertAlmostEqual(free_busy.time_min, time_min, delta=timedelta(seconds=5))
        self.assertAlmostEqual(free_busy.time_max, time_max, delta=timedelta(seconds=5))

        self.assertEqual(len(free_busy.calendars), 1)
        self.assertEqual(len(free_busy.calendars['primary']), 2)
        self.assertTrue(
            all(
                time_range_within(tr, time_min, time_max)
                for tr in free_busy.calendars['primary']
            )
        )

    def test_query_with_resource_ids(self):
        time_min = ensure_localisation(D.now())
        time_max = time_min + 2 * weeks

        free_busy = self.gc.get_free_busy(resource_ids='calendar3')

        self.assertEqual(len(free_busy.calendars), 1)
        self.assertIn('calendar3', free_busy.calendars)
        self.assertTrue(
            all(
                time_range_within(tr, time_min, time_max)
                for tr in free_busy.calendars['calendar3']
            )
        )

        free_busy = self.gc.get_free_busy(resource_ids=['primary', 'group2'])

        self.assertEqual(len(free_busy.calendars), 3)
        # by calendar id
        self.assertIn('primary', free_busy.calendars)
        # by group
        self.assertIn('calendar3', free_busy.calendars)
        self.assertIn('calendar4', free_busy.calendars)

        self.assertTrue(
            all(
                time_range_within(tr, time_min, time_max)
                for tr in free_busy.calendars['primary']
            )
        )
        self.assertTrue(
            all(
                time_range_within(tr, time_min, time_max)
                for tr in free_busy.calendars['calendar3']
            )
        )

        self.assertTrue(len(free_busy.groups), 1)
        self.assertIn('group2', free_busy.groups)

    def test_query_with_errors(self):
        with self.assertRaises(FreeBusyQueryError) as cm:
            self.gc.get_free_busy(resource_ids=['calendar-unknown'])
        fb_exception = cm.exception
        self.assertIn('calendar-unknown', fb_exception.calendars_errors)

        with self.assertRaises(FreeBusyQueryError) as cm:
            self.gc.get_free_busy(resource_ids=['group-unknown'])
        fb_exception = cm.exception
        self.assertIn('group-unknown', fb_exception.groups_errors)

    def test_query_with_errors_ignored(self):
        free_busy = self.gc.get_free_busy(resource_ids=['calendar-unknown', 'group-unknown'], ignore_errors=True)
        self.assertIn('calendar-unknown', free_busy.calendars_errors)
        self.assertIn('group-unknown', free_busy.groups_errors)
        self.assertFalse(free_busy.calendars)
        self.assertFalse(free_busy.groups)
