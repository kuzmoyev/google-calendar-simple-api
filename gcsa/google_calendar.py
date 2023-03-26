from google.oauth2.credentials import Credentials

from ._services.acl_service import ACLService
from ._services.events_service import EventsService, SendUpdatesMode  # noqa: F401
from ._services.calendars_service import CalendarsService
from ._services.calendar_lists_service import CalendarListService
from ._services.colors_service import ColorsService
from ._services.free_busy_service import FreeBusyService
from ._services.settings_service import SettingsService


class GoogleCalendar(
    EventsService,
    CalendarsService,
    CalendarListService,
    ColorsService,
    SettingsService,
    ACLService,
    FreeBusyService
):
    """Collection of all supported methods for events and calendars management."""

    def __init__(
            self,
            default_calendar: str = 'primary',
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

        :param default_calendar:
                Users email address or name/id of the calendar. Default: primary calendar of the user

                If user's email or "primary" is specified, then primary calendar of the user is used.
                You don't need to specify this parameter in this case as it is a default behaviour.

                To use a different calendar you need to specify its id.
                Go to calendar's `settings and sharing` -> `Integrate calendar` -> `Calendar ID`.
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
        super().__init__(
            default_calendar=default_calendar,
            credentials=credentials,
            credentials_path=credentials_path,
            token_path=token_path,
            save_token=save_token,
            read_only=read_only,
            authentication_flow_host=authentication_flow_host,
            authentication_flow_port=authentication_flow_port
        )
