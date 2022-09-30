from unittest import TestCase

from gcsa.serializers.settings_serializer import SettingsSerializer
from gcsa.settings import Settings


class TestSettings(TestCase):
    def test_repr_str(self):
        settings = Settings(
            auto_add_hangouts=True,
            date_field_order='DMY',
            default_event_length=45,
            format24_hour_time=True,
            hide_invitations=True,
            hide_weekends=True,
            locale='cz',
            remind_on_responded_events_only=True,
            show_declined_events=False,
            timezone='Europe/Prague',
            use_keyboard_shortcuts=False,
            week_start=1,
        )
        expected_str = \
            "User settings:\n" \
            "auto_add_hangouts=True\n" \
            "date_field_order=DMY\n" \
            "default_event_length=45\n" \
            "format24_hour_time=True\n" \
            "hide_invitations=True\n" \
            "hide_weekends=True\n" \
            "locale=cz\n" \
            "remind_on_responded_events_only=True\n" \
            "show_declined_events=False\n" \
            "timezone=Europe/Prague\n" \
            "use_keyboard_shortcuts=False\n" \
            "week_start=1"
        self.assertEqual(settings.__str__(), expected_str)
        self.assertEqual(settings.__repr__(), expected_str)


class TestSettingsSerializer(TestCase):
    def test_to_json(self):
        settings = Settings(
            auto_add_hangouts=True,
            date_field_order='DMY',
            default_event_length=45,
            format24_hour_time=True,
            hide_invitations=True,
            hide_weekends=True,
            locale='cz',
            remind_on_responded_events_only=True,
            show_declined_events=False,
            timezone='Europe/Prague',
            use_keyboard_shortcuts=False,
            week_start=1,
        )
        expected_json = {
            'autoAddHangouts': settings.auto_add_hangouts,
            'dateFieldOrder': settings.date_field_order,
            'defaultEventLength': settings.default_event_length,
            'format24HourTime': settings.format24_hour_time,
            'hideInvitations': settings.hide_invitations,
            'hideWeekends': settings.hide_weekends,
            'locale': settings.locale,
            'remindOnRespondedEventsOnly': settings.remind_on_responded_events_only,
            'showDeclinedEvents': settings.show_declined_events,
            'timezone': settings.timezone,
            'useKeyboardShortcuts': settings.use_keyboard_shortcuts,
            'weekStart': settings.week_start
        }
        self.assertDictEqual(SettingsSerializer(settings).get_json(), expected_json)

    def test_to_object(self):
        settings_json = {
            'autoAddHangouts': True,
            'dateFieldOrder': 'DMY',
            'defaultEventLength': 45,
            'format24HourTime': True,
            'hideInvitations': True,
            'hideWeekends': True,
            'locale': 'cz',
            'remindOnRespondedEventsOnly': True,
            'showDeclinedEvents': False,
            'timezone': 'Europe/Prague',
            'useKeyboardShortcuts': False,
            'weekStart': 1,
        }
        settings = SettingsSerializer(settings_json).get_object()

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
