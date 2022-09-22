from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from gcsa.google_calendar import GoogleCalendar
from tests.mock_services.mock_service import MockService


class MockToken:
    def __init__(self, valid, refresh_token='refresh_token'):
        self.valid = valid
        self.expired = not valid
        self.refresh_token = refresh_token

    def refresh(self, _):
        self.valid = True
        self.expired = False


class TestCaseWithMockedService(TestCase):
    def setUp(self):
        self.build_patcher = patch('googleapiclient.discovery.build', return_value=MockService())
        self.build_patcher.start()

        self.gc = GoogleCalendar(credentials=MockToken(valid=True))

    def tearDown(self):
        self.build_patcher.stop()


def executable(fn):
    """Decorator that stores data received from the function in object that returns that data when
    called its `execute` method. Emulates HttpRequest from googleapiclient."""

    class Executable:
        def __init__(self, data):
            self.data = data

        def execute(self):
            return self.data

    def wrapper(*args, **kwargs):
        data = fn(*args, **kwargs)
        return Executable(data)

    return wrapper
