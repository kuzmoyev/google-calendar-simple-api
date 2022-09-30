from gcsa.settings import Settings
from .base_serializer import BaseSerializer


class SettingsSerializer(BaseSerializer):
    type_ = Settings

    def __init__(self, settings):
        super().__init__(settings)

    @staticmethod
    def _to_json(settings: Settings):
        """Isn't used as Settings are read-only"""
        return {
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

    @staticmethod
    def _to_object(json_settings):
        return Settings(
            auto_add_hangouts=json_settings.get('autoAddHangouts', False),
            date_field_order=json_settings.get('dateFieldOrder', 'MDY'),
            default_event_length=json_settings.get('defaultEventLength', 60),
            format24_hour_time=json_settings.get('format24HourTime', False),
            hide_invitations=json_settings.get('hideInvitations', False),
            hide_weekends=json_settings.get('hideWeekends', False),
            locale=json_settings.get('locale', 'en'),
            remind_on_responded_events_only=json_settings.get('remindOnRespondedEventsOnly', False),
            show_declined_events=json_settings.get('showDeclinedEvents', True),
            timezone=json_settings.get('timezone', 'Etc/GMT'),
            use_keyboard_shortcuts=json_settings.get('useKeyboardShortcuts', True),
            week_start=json_settings.get('weekStart', 0)
        )
