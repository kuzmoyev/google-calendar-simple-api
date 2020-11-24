import pickle
from os import path
from pyfakefs.fake_filesystem_unittest import TestCase

from unittest.mock import patch

from gcsa.google_calendar import GoogleCalendar

TEST_TIMEZONE = 'Pacific/Fiji'


class MockToken:
    def __init__(self, valid, refresh_token='refresh_token'):
        self.valid = valid
        self.expired = not valid
        self.refresh_token = refresh_token

    def refresh(self, _):
        self.valid = True
        self.expired = False


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
            def run_local_server(self):
                return MockToken(valid=True)

        self.from_client_secrets_file = patch(
            'google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file',
            return_value=MockAuthFlow()
        ).start()

    def tearDown(self):
        self.build_patcher.stop()
        self.from_client_secrets_file.stop()

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
        self.assertTrue(gc.token.valid)
        self.assertFalse(self.from_client_secrets_file.called)

    def test_get_token_expired(self):
        gc = GoogleCalendar(token_path=self.expired_token_path)
        self.assertTrue(gc.token.valid)
        self.assertFalse(gc.token.expired)
        self.assertFalse(self.from_client_secrets_file.called)

    def test_get_token_invalid_refresh(self):
        gc = GoogleCalendar(credentials_path=self.credentials_path)
        self.assertTrue(gc.token.valid)
        self.assertFalse(gc.token.expired)
        self.assertTrue(self.from_client_secrets_file.called)
