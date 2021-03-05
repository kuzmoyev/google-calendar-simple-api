from datetime import date, datetime
import pickle
import os.path
from typing import List, Union, Callable

from beautiful_date import BeautifulDate
from dateutil.relativedelta import relativedelta
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tzlocal import get_localzone

from google.oauth2.credentials import Credentials

from .serializers.event_serializer import EventSerializer
from .util.date_time_util import insure_localisation


class SendUpdatesMode:
    """ Possible values of the mode for sending updates or invitations to attendees.

    * ALL - Send updates to all participants. This is the default value.
    * EXTERNAL_ONLY - Send updates only to attendees not using google calendar.
    * NONE - Do not send updates.
    """

    ALL = "all"
    EXTERNAL_ONLY = "externalOnly"
    NONE = "none"


class GoogleCalendar:
    _READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/calendar'
    _LIST_ORDERS = ("startTime", "updated")

    def __init__(
            self,
            calendar: str = 'primary',
            *,
            credentials: Credentials = None,
            credentials_path: str = None,
            token_path: str = None,
            save_token: bool = True,
            read_only: bool = False,
            authentication_flow_host='localhost',
            authentication_flow_port=8080
    ):
        """Represents Google Calendar of the user.

        Specify ``credentials`` to use in requests or ``credentials_path`` and ``token_path`` to get credentials from.

        :param calendar:
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

        if credentials:
            self.credentials = self._assure_refreshed(credentials)
        else:
            credentials_path = credentials_path or GoogleCalendar._get_default_credentials_path()
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

        self.calendar = calendar
        self.service = discovery.build('calendar', 'v3', credentials=self.credentials)

    @staticmethod
    def _assure_refreshed(credentials: Credentials):
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
        """ Checks if ".credentials" folder in home directory exists. If not, creates it.
        :return: expanded path to .credentials folder
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'credentials.json')
        return credential_path

    def clear(self):
        """Deletes all the events in the calendar"""
        self.service.calendars().clear(calendarId=self.calendar).execute()

    def add_event(
            self,
            event,
            send_updates=SendUpdatesMode.NONE,
            **kwargs
    ):
        """Creates event in the calendar

        :param event:
                Event object.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/insert#optional-parameters

        :return:
                Created event object with id.
        """
        body = EventSerializer(event).get_json()
        event_json = self.service.events().insert(
            calendarId=self.calendar,
            body=body,
            conferenceDataVersion=1,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def add_quick_event(
            self,
            event_string,
            send_updates=SendUpdatesMode.NONE,
            **kwargs
    ):
        """Creates event in the calendar by string description.

        Example:
            Appointment at Somewhere on June 3rd 10am-10:25am

        :param event_string:
                String that describes an event
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/quickAdd#optional-parameters

        :return:
                Created event object with id.
        """
        event_json = self.service.events().quickAdd(
            calendarId=self.calendar,
            text=event_string,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def import_event(self, event, **kwargs):
        """Imports an event in the calendar

        This operation is used to add a private copy of an existing event to a calendar.

        :param event:
                Event object.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/import#optional-parameters

        :return:
                Created event object with id.
        """
        body = EventSerializer(event).get_json()
        event_json = self.service.events().import_(
            calendarId=self.calendar,
            body=body,
            conferenceDataVersion=1,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def update_event(
            self,
            event,
            send_updates=SendUpdatesMode.NONE,
            **kwargs
    ):
        """Updates existing event in the calendar

        :param event:
                Event object with set event_id.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/update#optional-parameters

        :return:
                Updated event object.
        """
        body = EventSerializer(event).get_json()
        event_json = self.service.events().update(
            calendarId=self.calendar,
            eventId=event.id,
            body=body,
            conferenceDataVersion=1,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def move_event(
            self,
            event,
            destination_calendar_id,
            send_updates=SendUpdatesMode.NONE,
            **kwargs
    ):
        """Moves existing event from calendar to another calendar

        :param event:
                Event object with set event_id.
        :param destination_calendar_id:
                Id of the destination calendar.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/move#optional-parameters

        :return:
                Moved event object.
        """
        moved_event_json = self.service.events().move(
            calendarId=self.calendar,
            eventId=event.id,
            destination=destination_calendar_id,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(moved_event_json)

    def delete_event(
            self,
            event,
            send_updates=SendUpdatesMode.NONE,
            **kwargs
    ):
        """ Deletes an event.

        :param event:
                Event object with set event_id.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/delete#optional-parameters
        """
        if event.id is None:
            raise ValueError("Event has to have event_id to be deleted.")
        self.service.events().delete(
            calendarId=self.calendar,
            eventId=event.id,
            sendUpdates=send_updates,
            **kwargs
        ).execute()

    def _list_events(
            self,
            request_method: Callable,
            time_min: Union[date, datetime, BeautifulDate],
            time_max: Union[date, datetime, BeautifulDate],
            timezone: str,
            **kwargs
    ):
        """Lists paginated events received from request_method."""

        time_min = time_min or datetime.now()
        time_max = time_max or time_min + relativedelta(years=1)

        if not isinstance(time_min, datetime):
            time_min = datetime.combine(time_min, datetime.min.time())

        if not isinstance(time_max, datetime):
            time_max = datetime.combine(time_max, datetime.max.time())

        time_min = insure_localisation(time_min, timezone).isoformat()
        time_max = insure_localisation(time_max, timezone).isoformat()

        page_token = None
        while True:
            events = request_method(
                calendarId=self.calendar,
                timeMin=time_min,
                timeMax=time_max,
                pageToken=page_token,
                **kwargs
            ).execute()
            for event_json in events['items']:
                event = EventSerializer(event_json).get_object()
                yield event
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def get_events(
            self,
            time_min=None,
            time_max=None,
            order_by=None,
            timezone=str(get_localzone()),
            single_events=False,
            query=None,
            **kwargs
    ):
        """ Lists events

        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param order_by:
                Order of the events. Possible values: "startTime", "updated". Default is unspecified stable order.
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param single_events:
                Whether to expand recurring events into instances and only return single one-off events and
                instances of recurring events, but not the underlying recurring events themselves.
        :param query:
                Free text search terms to find events that match these terms in any field, except for
                extended properties.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/list#optional-parameters

        :return:
                Iterable of event objects
        """

        if not single_events and order_by == 'startTime':
            raise ValueError(
                '"startTime" ordering is only available when querying single events, i.e. single_events=True'
            )

        yield from self._list_events(
            self.service.events().list,
            time_min=time_min,
            time_max=time_max,
            timezone=timezone,
            **{
                'singleEvents': single_events,
                'orderBy': order_by,
                'q': query,
                **kwargs
            }
        )

    def get_instances(
            self,
            recurring_event,
            time_min=None,
            time_max=None,
            timezone=str(get_localzone()),
            **kwargs
    ):
        """ Lists instances of recurring event

        :param recurring_event:
                Recurring event (Event object) or id of a recurring event
        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/instances#optional-parameters

        :return:
                Iterable of event objects
        """
        yield from self._list_events(
            self.service.events().instances,
            time_min=time_min,
            time_max=time_max,
            timezone=timezone,
            **{
                'eventId': recurring_event if isinstance(recurring_event, str) else recurring_event.id,
                **kwargs
            }
        )

    def get_event(self, event_id, **kwargs):
        """ Returns the event with the corresponding event_id.

        :param event_id:
                The unique event ID.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/get#optional-parameters

        :return:
                The corresponding event object or None if
                no matching ID was found.
        """
        event_resource = self.service.events().get(
            calendarId=self.calendar,
            eventId=event_id,
            **kwargs
        ).execute()
        return EventSerializer(event_resource).get_object()

    def list_event_colors(self):
        """List allowed event colors for the calendar."""
        return self.service.colors().get().execute()['event']

    def __iter__(self):
        return iter(self.get_events())

    def __getitem__(self, r):
        if isinstance(r, slice):
            time_min, time_max, order_by = r.start or None, r.stop or None, r.step or None
        elif isinstance(r, (date, datetime)):
            time_min, time_max, order_by = r, None, None
        else:
            raise NotImplementedError

        if (
                (time_min and not isinstance(time_min, (date, datetime)))
                or (time_max and not isinstance(time_max, (date, datetime)))
                or (order_by and (not isinstance(order_by, str) or order_by not in self._LIST_ORDERS))
        ):
            raise ValueError('Calendar indexing is in the following format:  time_min[:time_max[:order_by]],'
                             ' where time_min and time_max are date/datetime objects'
                             ' and order_by is None or one of "startTime" or "updated" strings.')

        return self.get_events(time_min, time_max, order_by=order_by, single_events=(order_by == "startTime"))
