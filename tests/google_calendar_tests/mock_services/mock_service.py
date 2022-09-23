from .mock_calendar_list_requests import MockCalendarListRequests
from .mock_calendars_requests import MockCalendarsRequests
from .mock_events_requests import MockEventsRequests


class MockService:
    """Emulates GoogleCalendar.service"""

    def __init__(self):
        self._events = MockEventsRequests()
        self._calendars = MockCalendarsRequests()
        self._calendar_list = MockCalendarListRequests()

    def events(self):
        return self._events

    def calendars(self):
        return self._calendars

    def calendarList(self):
        return self._calendar_list
