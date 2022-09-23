import pickle
from os import path
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from gcsa.google_calendar import GoogleCalendar
from tests.google_calendar_tests.mock_services.util import MockToken


class TestGoogleCalendarCredentials(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        self.credentials_dir = '/.credentials'
        self.credentials_path = path.join(self.credentials_dir, 'credentials.json')
        self.fs.create_dir(self.credentials_dir)
        self.fs.create_file(self.credentials_path)

        self.valid_token_path = path.join(self.credentials_dir, 'valid_token.pickle')
        self.expired_token_path = path.join(self.credentials_dir, 'expired_token.pickle')

        with open(self.valid_token_path, 'wb') as token_file:
            pickle.dump(MockToken(valid=True), token_file)
        with open(self.expired_token_path, 'wb') as token_file:
            pickle.dump(MockToken(valid=False), token_file)

        self._add_mocks()

    def _add_mocks(self):
        self.build_patcher = patch('googleapiclient.discovery.build', return_value=None).start()

        class MockAuthFlow:
            def run_local_server(self, *args, **kwargs):
                return MockToken(valid=True)

        self.from_client_secrets_file_patcher = patch(
            'google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file',
            return_value=MockAuthFlow()
        ).start()

    def tearDown(self):
        self.build_patcher.stop()
        self.from_client_secrets_file_patcher.stop()

    def test_with_given_credentials(self):
        GoogleCalendar(credentials=MockToken(valid=True))
        self.assertFalse(self.from_client_secrets_file_patcher.called)

    def test_with_given_credentials_expired(self):
        gc = GoogleCalendar(credentials=MockToken(valid=False))
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(gc.credentials.expired)

    def test_get_default_credentials_path_exist(self):
        self.fs.create_dir(path.join(path.expanduser('~'), '.credentials'))
        self.assertEqual(
            path.join(path.expanduser('~'), '.credentials/credentials.json'),
            GoogleCalendar._get_default_credentials_path()
        )

    def test_get_default_credentials_path_not_exist(self):
        self.assertFalse(path.exists(path.join(path.expanduser('~'), '.credentials')))
        self.assertEqual(
            path.join(path.expanduser('~'), '.credentials/credentials.json'),
            GoogleCalendar._get_default_credentials_path()
        )
        self.assertTrue(path.exists(path.join(path.expanduser('~'), '.credentials')))

    def test_get_token_valid(self):
        gc = GoogleCalendar(token_path=self.valid_token_path)
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(self.from_client_secrets_file_patcher.called)

    def test_get_token_expired(self):
        gc = GoogleCalendar(token_path=self.expired_token_path)
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(gc.credentials.expired)
        self.assertFalse(self.from_client_secrets_file_patcher.called)

    def test_get_token_invalid_refresh(self):
        gc = GoogleCalendar(credentials_path=self.credentials_path)
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(gc.credentials.expired)
        self.assertTrue(self.from_client_secrets_file_patcher.called)
