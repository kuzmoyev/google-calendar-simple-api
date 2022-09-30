from .util import executable


class MockSettingsRequests:
    """Emulates GoogleCalendar.service.settings()"""

    @executable
    def list(self, **_):
        """Emulates GoogleCalendar.service.settings().list().execute()"""
        return {
            "nextPageToken": None,
            "items": [
                {'id': 'autoAddHangouts', 'value': True},
                {'id': 'dateFieldOrder', 'value': 'DMY'},
                {'id': 'defaultEventLength', 'value': 45},
                {'id': 'format24HourTime', 'value': True},
                {'id': 'hideInvitations', 'value': True},
                {'id': 'hideWeekends', 'value': True},
                {'id': 'locale', 'value': 'cz'},
                {'id': 'remindOnRespondedEventsOnly', 'value': True},
                {'id': 'showDeclinedEvents', 'value': False},
                {'id': 'timezone', 'value': 'Europe/Prague'},
                {'id': 'useKeyboardShortcuts', 'value': False},
                {'id': 'weekStart', 'value': 1}
            ]
        }
