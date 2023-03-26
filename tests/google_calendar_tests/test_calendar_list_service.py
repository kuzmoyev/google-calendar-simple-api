from gcsa.calendar import CalendarListEntry, Calendar
from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestCalendarListService(TestCaseWithMockedService):
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
        self.assertEqual(calendar.summary_override, new_calendar.summary_override)

    def test_update_calendar_list_entry(self):
        calendar = CalendarListEntry(
            calendar_id='test_calendar_list_entry',
            _summary='Summary',
            summary_override='Summary override'
        )
        new_calendar = self.gc.add_calendar_list_entry(calendar)

        self.assertEqual(calendar.summary_override, new_calendar.summary_override)

        new_calendar.summary_override = 'Updated summary override'
        updated_calendar = self.gc.update_calendar_list_entry(new_calendar)

        self.assertEqual(new_calendar.summary_override, updated_calendar.summary_override)

        retrieved_updated_calendar = self.gc.get_calendar_list_entry(new_calendar.id)
        self.assertEqual(retrieved_updated_calendar.summary_override, updated_calendar.summary_override)

    def test_delete_calendar_list_entry(self):
        calendar = Calendar(
            summary='Summary'
        )
        with self.assertRaises(ValueError):
            # no calendar_id
            self.gc.delete_calendar_list_entry(calendar)

        calendar = CalendarListEntry(
            calendar_id='test_calendar_list_entry',
            _summary='Summary',
            summary_override='Summary override'
        )

        self.gc.delete_calendar_list_entry(calendar)
        self.gc.delete_calendar_list_entry('2')

        with self.assertRaises(TypeError):
            # should be a Calendar, CalendarListEntry or calendar id as a string
            self.gc.delete_calendar_list_entry(calendar=None)
