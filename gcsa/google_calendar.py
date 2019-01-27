import datetime
import pickle
import os.path

from beautiful_date import Jan, Apr
from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tzlocal import get_localzone

from event import Event
from recurrence import Recurrence, DAILY, SU, SA
from serializers.event_serializer import EventSerializer
from util.date_time_util import insure_localisation


def _get_default_credentials_path():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python.json')
    return credential_path


class GoogleCalendar:
    _READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/calendar'

    def __init__(self,
                 calendar,
                 credentials_path=_get_default_credentials_path(),
                 read_only=False,
                 application_name=None):

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
        body = EventSerializer(event).get_json()
        return self.service.events().insert(calendarId=self.calendar, body=body).execute()

    def add_quick_event(self, event_string):
        return self.service.events().quickAdd(calendarId=self.calendar, text=event_string).execute()

    def delete_event(self, event):
        return self.service.events().delete(calendarId=self.calendar, eventId=event.get_id()).execute()

    def get_events(self, time_min=None, time_max=None, order_by='startTime', timezone=str(get_localzone())):
        time_min = time_min or datetime.datetime.utcnow()
        time_max = time_max or time_min + relativedelta(years=1)

        time_min = insure_localisation(time_min, timezone).isoformat()
        time_max = insure_localisation(time_max, timezone).isoformat()

        res = []
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
                res.append(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return res

    def list_event_colors(self):
        return self.service.colors().get().execute()['event']


def main():
    calendar = GoogleCalendar('kuzmovich.goog@gmail.com', '../credentials.json')
    event = Event(
        'Breakfast',
        start=(1 / Jan / 2019)[9:00],
        recurrence=[
            Recurrence.rule(freq=DAILY),
            Recurrence.exclude_rule(by_week_day=[SU, SA]),
            Recurrence.exclude_times([
                (19 / Apr / 2019)[9:00],
                (22 / Apr / 2019)[9:00]
            ])
        ],
        minutes_before_email_reminder=50
    )

    for event in calendar.get_events():
        print(event)


if __name__ == '__main__':
    main()
