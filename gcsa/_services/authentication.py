import logging
import pickle
import os.path
import glob
import webbrowser
from typing import List, Optional

from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials

log = logging.getLogger(__name__)


class AuthenticatedService:
    """Handles authentication of the `GoogleCalendar`"""

    _READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/calendar'

    def __init__(
            self,
            *,
            credentials: Optional[Credentials] = None,
            credentials_path: Optional[str] = None,
            token_path: Optional[str] = None,
            save_token: bool = True,
            read_only: bool = False,
            authentication_flow_host: str = 'localhost',
            authentication_flow_port: int = 8080,
            authentication_flow_bind_addr: Optional[str] = None,
            open_browser: Optional[bool] = None
    ):
        """
        Specify ``credentials`` to use in requests or ``credentials_path`` and ``token_path`` to get credentials from.

        :param credentials:
                Credentials with token and refresh token.
                If specified, ``credentials_path``, ``token_path``, and ``save_token`` are ignored.
                If not specified, credentials are retrieved from "token.pickle" file (specified in ``token_path`` or
                default path) or with authentication flow using secret from "credentials.json" ("client_secret_*.json")
                (specified in ``credentials_path`` or default path)
        :param credentials_path:
                Path to "credentials.json" ("client_secret_*.json") file.
                Default: ~/.credentials/credentials.json or ~/.credentials/client_secret*.json
        :param token_path:
                Existing path to load the token from, or path to save the token after initial authentication flow.
                Default: "token.pickle" in the same directory as the credentials_path
        :param save_token:
                Whether to pickle token after authentication flow for future uses
        :param read_only:
                If require read-only access. Default: False
        :param authentication_flow_host:
                Host to receive response during authentication flow
        :param authentication_flow_port:
                Port to receive response during authentication flow
        :param authentication_flow_bind_addr:
                Optional IP address for the redirect server to listen on when it is different from host
                (e.g., in a container)
        :param open_browser:
                Whether to open the authorization URL in the user's browser.
                    - `None` (default): try opening the URL in the browser, if it fails proceed without the browser
                    - `True`: try opening the URL in the browser,
                      raise `webbrowser.Error` if runnable browser can not be located
                    - `False`: do not open URL in the browser.
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
                authentication_flow_port,
                authentication_flow_bind_addr,
                open_browser
            )

        self.service = discovery.build('calendar', 'v3', credentials=self.credentials)

    @staticmethod
    def _ensure_refreshed(
            credentials: Credentials
    ) -> Credentials:
        if not credentials.valid and credentials.expired:
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
            port: int,
            bind_addr: Optional[str],
            open_browser: Optional[bool]
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
                try:
                    credentials = flow.run_local_server(
                        host=host,
                        port=port,
                        bind_addr=bind_addr,
                        open_browser=open_browser or open_browser is None
                    )
                except webbrowser.Error:
                    if open_browser:
                        raise
                    else:
                        # Try without a browser
                        log.warning("Could not locate runnable browser")
                        credentials = flow.run_local_server(
                            host=host,
                            port=port,
                            bind_addr=bind_addr,
                            open_browser=False
                        )

            if save_token:
                with open(token_path, 'wb') as token_file:
                    pickle.dump(credentials, token_file)

        return credentials

    @staticmethod
    def _get_default_credentials_path() -> str:
        """Checks if `.credentials` folder in home directory exists and contains `credentials.json` or
        `client_secret*.json` file.

        :raises ValueError: if `.credentials` folder does not exist, none of `credentials.json` or `client_secret*.json`
        files do not exist, or there are multiple `client_secret*.json` files.
        :return: expanded path to `credentials.json` or `client_secret*.json` file
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            raise FileNotFoundError(f'Default credentials directory "{credential_dir}" does not exist.')
        credential_path = os.path.join(credential_dir, 'credentials.json')
        if os.path.exists(credential_path):
            return credential_path
        else:
            credentials_files = glob.glob(credential_dir + '/client_secret*.json')
            if len(credentials_files) > 1:
                raise ValueError(f"Multiple credential files found in {credential_dir}.\n"
                                 f"Try specifying the credentials file, e.x.:\n"
                                 f"GoogleCalendar(credentials_path='{credentials_files[0]}')")
            elif not credentials_files:
                raise FileNotFoundError(f'Credentials file (credentials.json or client_secret*.json)'
                                        f'not found in the default path: "{credential_dir}".')
            else:
                return credentials_files[0]
