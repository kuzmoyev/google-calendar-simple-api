from gcsa.calendar import Calendar, AccessRoles
from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestEventsService(TestCaseWithMockedService):
    def test_get_calendar(self):
        calendar = self.gc.get_calendar()
        self.assertEqual(calendar.id, 'primary')

        calendar = self.gc.get_calendar('1')
        self.assertEqual(calendar.id, '1')

    def test_add_calendar(self):
        calendar = Calendar(
            summary='secondary',
            description='Description secondary',
            location='Location secondary',
            timezone='Timezone secondary',
            allowed_conference_solution_types=[
                AccessRoles.FREE_BUSY_READER,
                AccessRoles.READER
            ]
        )
        new_calendar = self.gc.add_calendar(calendar)

        self.assertIsNotNone(new_calendar.id)
        self.assertEqual(calendar.summary, new_calendar.summary)

    def test_update_calendar(self):
        calendar = Calendar(
            summary='secondary',
            description='Description secondary',
            location='Location secondary',
            timezone='Timezone secondary',
            allowed_conference_solution_types=[
                AccessRoles.FREE_BUSY_READER,
                AccessRoles.READER
            ]
        )
        new_calendar = self.gc.add_calendar(calendar)

        self.assertEqual(calendar.summary, new_calendar.summary)

        new_calendar.summary = 'Updated summary'
        updated_calendar = self.gc.update_calendar(new_calendar)

        self.assertEqual(new_calendar.summary, updated_calendar.summary)

        retrieved_updated_calendar = self.gc.get_calendar(new_calendar.id)
        self.assertEqual(retrieved_updated_calendar.summary, updated_calendar.summary)

    def test_delete_calendar(self):
        calendar = Calendar(
            summary='secondary'
        )

        with self.assertRaises(ValueError):
            # no calendar_id
            self.gc.delete_calendar(calendar)

        new_calendar = self.gc.add_calendar(calendar)
        self.gc.delete_calendar(new_calendar)
        self.gc.delete_calendar('2')

        with self.assertRaises(TypeError):
            # should be a Calendar or calendar id as a string
            self.gc.delete_calendar(None)

    def test_clear_calendar(self):
        self.gc.clear_calendar()
        self.gc.clear()
