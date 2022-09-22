from .mock_calendars_requests import MockCalendarsRequests
from .mock_events_requests import MockEventsRequests


class MockService:
    """Emulates GoogleCalendar.service"""

    def __init__(self):
        self._events = MockEventsRequests()
        self._calendars = MockCalendarsRequests()

    def events(self):
        return self._events

    def calendars(self):
        return self._calendars
