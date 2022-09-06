import pickle
import os.path
from typing import List

from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class AuthenticatedService:
    """Handles authentication of the `GoogleCalendar`"""

    _READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/calendar'
    _LIST_ORDERS = ("startTime", "updated")

    def __init__(
            self,
            *,
            credentials: Credentials = None,
            credentials_path: str = None,
            token_path: str = None,
            save_token: bool = True,
            read_only: bool = False,
            authentication_flow_host: str = 'localhost',
            authentication_flow_port: int = 8080
    ):
        """
        Specify ``credentials`` to use in requests or ``credentials_path`` and ``token_path`` to get credentials from.

        :param credentials:
                Credentials with token and refresh token.
                If specified, ``credentials_path``, ``token_path``, and ``save_token`` are ignored.
                If not specified, credentials are retrieved from "token.pickle" file (specified in ``token_path`` or
                default path) or with authentication flow using secret from "credentials.json" (specified in
                ``credentials_path`` or default path)
        :param credentials_path:
                Path to "credentials.json" file. Default: ~/.credentials
        :param token_path:
                Existing path to load the token from, or path to save the token after initial authentication flow.
                Default: "token.pickle" in the same directory as the credentials_path
        :param save_token:
                Whether to pickle token after authentication flow for future uses
        :param read_only:
                If require read only access. Default: False
        :param authentication_flow_host:
                Host to receive response during authentication flow
        :param authentication_flow_port:
                Port to receive response during authentication flow
        """

        if credentials:
            self.credentials = self._ensure_refreshed(credentials)
        else:
            credentials_path = credentials_path or self._get_default_credentials_path()
            credentials_dir, credentials_file = os.path.split(credentials_path)
            token_path = token_path or os.path.join(credentials_dir, 'token.pickle')
            scopes = [self._READ_WRITE_SCOPES + ('.readonly' if read_only else '')]

            self.credentials = self._get_credentials(
                token_path,
                credentials_dir,
                credentials_file,
                scopes,
                save_token,
                authentication_flow_host,
                authentication_flow_port
            )

        self.service = discovery.build('calendar', 'v3', credentials=self.credentials)

    @staticmethod
    def _ensure_refreshed(
            credentials: Credentials
    ) -> Credentials:
        if not credentials.valid and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        return credentials

    @staticmethod
    def _get_credentials(
            token_path: str,
            credentials_dir: str,
            credentials_file: str,
            scopes: List[str],
            save_token: bool,
            host: str,
            port: int
    ) -> Credentials:
        credentials = None

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token_file:
                credentials = pickle.load(token_file)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials_path = os.path.join(credentials_dir, credentials_file)
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                credentials = flow.run_local_server(host=host, port=port)

            if save_token:
                with open(token_path, 'wb') as token_file:
                    pickle.dump(credentials, token_file)

        return credentials

    @staticmethod
    def _get_default_credentials_path() -> str:
        """Checks if ".credentials" folder in home directory exists. If not, creates it.
        :return: expanded path to .credentials folder
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'credentials.json')
        return credential_path
