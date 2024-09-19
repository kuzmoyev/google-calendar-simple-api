import pickle
import webbrowser
from os import path
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from gcsa.google_calendar import GoogleCalendar
from tests.google_calendar_tests.mock_services.util import MockToken, MockAuthFlow


class TestGoogleCalendarCredentials(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        self.credentials_dir = path.join(path.expanduser('~'), '.credentials')
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

        self.from_client_secrets_file_patcher = patch(
            'google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file',
            return_value=MockAuthFlow()
        ).start()

    def test_with_given_credentials(self):
        GoogleCalendar(credentials=MockToken(valid=True))
        self.assertFalse(self.from_client_secrets_file_patcher.called)

    def test_with_given_credentials_expired(self):
        gc = GoogleCalendar(credentials=MockToken(valid=False))
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(gc.credentials.expired)

    def test_get_default_credentials_exist(self):
        self.assertEqual(
            self.credentials_path,
            GoogleCalendar._get_default_credentials_path()
        )

    def test_get_default_credentials_path_not_exist(self):
        self.fs.reset()
        with self.assertRaises(FileNotFoundError):
            GoogleCalendar._get_default_credentials_path()

    def test_get_default_credentials_not_exist(self):
        self.fs.remove(self.credentials_path)
        with self.assertRaises(FileNotFoundError):
            GoogleCalendar._get_default_credentials_path()

    def test_get_default_credentials_client_secrets(self):
        self.fs.remove(self.credentials_path)
        client_secret_path = path.join(self.credentials_dir, 'client_secret_1234.json')
        self.fs.create_file(client_secret_path)
        self.assertEqual(
            client_secret_path,
            GoogleCalendar._get_default_credentials_path()
        )

    def test_get_default_credentials_multiple_client_secrets(self):
        self.fs.remove(self.credentials_path)
        self.fs.create_file(path.join(self.credentials_dir, 'client_secret_1234.json'))
        self.fs.create_file(path.join(self.credentials_dir, 'client_secret_12345.json'))
        with self.assertRaises(ValueError):
            GoogleCalendar._get_default_credentials_path()

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

    def test_no_browser_without_error(self):
        self.from_client_secrets_file_patcher = patch(
            'google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file',
            return_value=MockAuthFlow(has_browser=False)
        ).start()

        gc = GoogleCalendar(credentials_path=self.credentials_path, open_browser=None)
        self.assertTrue(gc.credentials.valid)
        self.assertTrue(self.from_client_secrets_file_patcher.called)

    def test_no_browser_with_error(self):
        self.from_client_secrets_file_patcher = patch(
            'google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file',
            return_value=MockAuthFlow(has_browser=False)
        ).start()

        with self.assertRaises(webbrowser.Error):
            GoogleCalendar(credentials_path=self.credentials_path, open_browser=True)
