from .mock_events_requests import MockEventsRequests


class MockService:
    @staticmethod
    def events():
        return MockEventsRequests()
