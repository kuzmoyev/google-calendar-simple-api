from datetime import date, datetime
import pickle
import os.path

from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tzlocal import get_localzone

from .serializers.event_serializer import EventSerializer
from util.date_time_util import insure_localisation


def _get_default_credentials_path():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'credentials.json')
    return credential_path


class GoogleCalendar:
    _READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/calendar'
    _LIST_ORDERS = ("startTime", "updated")

    def __init__(self,
                 calendar='primary',
                 credentials_path=None,
                 read_only=False,
                 application_name=None):
        """Represents Google Calendar of the user.

        :param calendar:
                users email address or name of the calendar. Default: primary calendar of the user.
        :param credentials_path:
                path to "credentials.json" file. Default: ~/.credentials.
        :param read_only:
                if require read only access. Default: False
        :param application_name:
                name of the application. Default: None
        """
        credentials_path = credentials_path or _get_default_credentials_path()
        self._credentials_dir, self._credentials_file = os.path.split(credentials_path)

        self._scopes = self._READ_WRITE_SCOPES + ('.readonly' if read_only else '')
        self._application_name = application_name

        self.calendar = calendar
        credentials = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=credentials)

    def _get_credentials(self):
        _credentials_path = os.path.join(self._credentials_dir, self._credentials_file)
        _token_path = os.path.join(self._credentials_dir, 'token.pickle')

        credentials = None

        if os.path.exists(_token_path):
            with open(_token_path, 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(_credentials_path, self._scopes)
                credentials = flow.run_local_server()

            with open(_token_path, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def add_event(self, event):
        """Creates event in the calendar

        :param event:
                event object.

        :return:
                created event object with id.
        """
        body = EventSerializer(event).get_json()
        event_json = self.service.events().insert(calendarId=self.calendar, body=body).execute()
        return EventSerializer.to_object(event_json)

    def add_quick_event(self, event_string):
        """Creates event in the calendar by string description.

        Example:
            Appointment at Somewhere on June 3rd 10am-10:25am

        :param event_string:
                string that describes an event

        :return:
                created event object with id.
        """
        event_json = self.service.events().quickAdd(calendarId=self.calendar, text=event_string).execute()
        return EventSerializer.to_object(event_json)

    def delete_event(self, event):
        """ Deletes an event.

        :param event:
                event object with set event_id.
        """
        if event.id is None:
            raise ValueError('Event has to have event_id to be deleted.')
        self.service.events().delete(calendarId=self.calendar, eventId=event.id).execute()

    def get_events(self, time_min=None, time_max=None, order_by='startTime', timezone=str(get_localzone())):
        """ Lists events

        :param time_min:
                staring date/datetime
        :param time_max:
                ending date/datetime
        :param order_by:
                order of the events. Possible values: "startTime", "updated".
        :param timezone:
                timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers configured local timezone(if any) is used.
        """
        time_min = time_min or datetime.utcnow()
        time_max = time_max or time_min + relativedelta(years=1)

        if not isinstance(time_min, datetime):
            time_min = datetime.combine(time_min, datetime.min.time())

        if not isinstance(time_max, datetime):
            time_max = datetime.combine(time_max, datetime.max.time())

        time_min = insure_localisation(time_min, timezone).isoformat()
        time_max = insure_localisation(time_max, timezone).isoformat()

        page_token = None
        while True:
            events = self.service.events().list(calendarId=self.calendar,
                                                timeMin=time_min,
                                                timeMax=time_max,
                                                orderBy=order_by,
                                                singleEvents=True,
                                                pageToken=page_token).execute()
            for event_json in events['items']:
                event = EventSerializer(event_json).get_object()
                yield event
            page_token = events.get('nextPageToken')
            if not page_token:
                break

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
