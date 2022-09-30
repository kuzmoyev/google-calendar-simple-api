from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestSettingsService(TestCaseWithMockedService):
    def test_get_settings(self):
        settings = self.gc.get_settings()
        self.assertTrue(settings.auto_add_hangouts)
        self.assertEqual(settings.date_field_order, 'DMY')
        self.assertEqual(settings.default_event_length, 45)
        self.assertTrue(settings.format24_hour_time)
        self.assertTrue(settings.hide_invitations)
        self.assertTrue(settings.hide_weekends)
        self.assertEqual(settings.locale, 'cz')
        self.assertTrue(settings.remind_on_responded_events_only)
        self.assertFalse(settings.show_declined_events)
        self.assertEqual(settings.timezone, 'Europe/Prague')
        self.assertFalse(settings.use_keyboard_shortcuts)
        self.assertEqual(settings.week_start, 1)
