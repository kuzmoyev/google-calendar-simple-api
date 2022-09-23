from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from gcsa.google_calendar import GoogleCalendar
from tests.google_calendar_tests.mock_services.mock_service import MockService
from tests.google_calendar_tests.mock_services.util import MockToken


class TestCaseWithMockedService(TestCase):
    def setUp(self):
        self.build_patcher = patch('googleapiclient.discovery.build', return_value=MockService())
        self.build_patcher.start()

        self.gc = GoogleCalendar(credentials=MockToken(valid=True))

    def tearDown(self):
        self.build_patcher.stop()
