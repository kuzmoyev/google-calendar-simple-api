from datetime import date, datetime
import pickle
import os.path

from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tzlocal import get_localzone

from .serializers.event_serializer import EventSerializer
from .util.date_time_util import insure_localisation


def _get_default_credentials_path():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'credentials.json')
    return credential_path


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

    def __init__(self,
                 calendar='primary',
                 *,
                 credentials_path=None,
                 token_path=None,
                 read_only=False,
                 application_name=None
                 ):
        """Represents Google Calendar of the user.

        :param calendar:
                Users email address or name/id of the calendar. Default: primary calendar of the user
        :param credentials_path:
                Path to "credentials.json" file. Default: ~/.credentials
        :param token_path:
                Existing path to load the token from, or path to save the token after initial authentication flow.
                Default: "token.pickle" in the same directory as the credentials_path
        :param read_only:
                If require read only access. Default: False
        :param application_name:
                Name of the application. Default: None
        """
        credentials_path = credentials_path or _get_default_credentials_path()
        self._credentials_dir, self._credentials_file = os.path.split(credentials_path)

        self._scopes = [self._READ_WRITE_SCOPES + ('.readonly' if read_only else '')]
        self._application_name = application_name
        self._token_path = token_path or os.path.join(self._credentials_dir, 'token.pickle')

        self.calendar = calendar
        credentials = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=credentials)

    def _get_credentials(self):
        _credentials_path = os.path.join(self._credentials_dir, self._credentials_file)

        credentials = None

        if os.path.exists(self._token_path):
            with open(self._token_path, 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(_credentials_path, self._scopes)
                credentials = flow.run_local_server()

            with open(self._token_path, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def add_event(self, event, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Creates event in the calendar

        :param event:
                Event object.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/insert

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

    def add_quick_event(self, event_string, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Creates event in the calendar by string description.

        Example:
            Appointment at Somewhere on June 3rd 10am-10:25am

        :param event_string:
                String that describes an event
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/quickAdd

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

    def update_event(self, event, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Updates existing event in the calendar

        :param event:
                Event object with set event_id.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/update

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

    def move_event(self, event, destination_calendar_id, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Moves existing event from calendar to another calendar

        :param event:
                Event object with set event_id.
        :param destination_calendar_id:
                Id of the destination calendar.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/move

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

    def delete_event(self, event, send_updates=SendUpdatesMode.NONE, **kwargs):
        """ Deletes an event.

        :param event:
                Event object with set event_id.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/delete
        """
        if event.id is None:
            raise ValueError("Event has to have event_id to be deleted.")
        self.service.events().delete(
            calendarId=self.calendar,
            eventId=event.id,
            sendUpdates=send_updates,
            **kwargs
        ).execute()

    def get_events(self, time_min=None, time_max=None, order_by='startTime', timezone=str(get_localzone()), **kwargs):
        """ Lists events

        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param order_by:
                Order of the events. Possible values: "startTime", "updated".
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/list


        :return:
                Iterable of event objects
        """
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
            events = self.service.events().list(
                calendarId=self.calendar,
                timeMin=time_min,
                timeMax=time_max,
                orderBy=order_by,
                singleEvents=True,
                pageToken=page_token,
                **kwargs
            ).execute()
            for event_json in events['items']:
                event = EventSerializer(event_json).get_object()
                yield event
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def get_event(self, event_id, **kwargs):
        """ Returns the event with the corresponding event_id.

        :param event_id:
                The unique event ID.
        :param kwargs:
                Additional API parameters. See https://developers.google.com/calendar/v3/reference/events/get

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
            time_min, time_max, order_by = r.start or None, r.stop or None, r.step or 'startTime'
        elif isinstance(r, (date, datetime)):
            time_min, time_max, order_by = r, None, 'startTime'
        else:
            return NotImplemented

        if (time_min and not isinstance(time_min, date)) \
                or (time_max and not isinstance(time_max, date)) \
                or not isinstance(order_by, str) or order_by not in self._LIST_ORDERS:
            raise ValueError('Calendar indexing is in the following format:  time_min[:time_max[:order_by]],'
                             ' where time_min and time_max are date/datetime objects'
                             ' and order_by is one of "startTime" or "updated" strings.')

        return self.get_events(time_min, time_max, order_by)
