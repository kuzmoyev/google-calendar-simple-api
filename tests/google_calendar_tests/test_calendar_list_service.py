from gcsa.calendar import CalendarListEntry
from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestEventsService(TestCaseWithMockedService):
    def test_get_calendar_list(self):
        calendars = list(self.gc.get_calendar_list())
        self.assertEqual(len(calendars), 8)
        self.assertTrue(any(c.id == 'primary' for c in calendars))

    def test_get_calendar_list_entry(self):
        calendar = self.gc.get_calendar_list_entry()
        self.assertEqual(calendar.id, 'primary')
        self.assertIsInstance(calendar, CalendarListEntry)

        calendar = self.gc.get_calendar('1')
        self.assertEqual(calendar.id, '1')

    def test_add_calendar_list_entry(self):
        calendar = CalendarListEntry(
            calendar_id='test_calendar_list_entry',
            _summary='Summary',
            summary_override='Summary override'
        )
        new_calendar = self.gc.add_calendar_list_entry(calendar)

        self.assertIsNotNone(new_calendar.id)
        self.assertEqual(calendar.summary, new_calendar.summary)
        self.assertEqual(calendar.summary_override, new_calendar.summary_override)
