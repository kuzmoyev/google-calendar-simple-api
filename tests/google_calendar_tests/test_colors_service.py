from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestColorsService(TestCaseWithMockedService):
    def test_list_event_colors(self):
        event_colors = self.gc.list_event_colors()
        self.assertEqual(len(event_colors), 4)

    def test_list_calendar_colors(self):
        calendar_colors = self.gc.list_calendar_colors()
        self.assertEqual(len(calendar_colors), 5)
