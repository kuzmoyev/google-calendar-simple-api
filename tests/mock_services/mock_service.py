from .mock_events_requests import MockEventsRequests


class MockService:
    def __init__(self):
        self._events = MockEventsRequests()

    def events(self):
        return self._events
