import datetime
import httplib2
import os

from apiclient import discovery
from dateutil.relativedelta import relativedelta
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from tzlocal import get_localzone

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
    _DEFAULT_CLIENT_SECRET_FILE = 'client_secret.json'

    def __init__(self,
                 calendar,
                 credentials_path=_get_default_credentials_path(),
                 read_only=False,
                 secret_file=_DEFAULT_CLIENT_SECRET_FILE,
                 application_name=None):
        self._credentials_path = credentials_path
        self._scopes = self._READ_WRITE_SCOPES + ('.readonly' if read_only else '')
        self._secret_file = secret_file
        self._application_name = application_name

        self.calendar = calendar
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def _get_credentials(self):
        store = Storage(self._credentials_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self._secret_file, self._scopes)
            flow.user_agent = self._application_name
            credentials = tools.run_flow(flow, store)
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

        time_min = insure_localisation(time_min, timezone)
        time_max = insure_localisation(time_max, timezone)

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
                event = EventSerializer(event_json).get_event()
                res.append(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return res

    def list_event_colors(self):
        return self.service.colors().get().execute()['event']


def main():
    calendar = GoogleCalendar('kuzmovich.goog@gmail.com')
    for color_id, color in calendar.list_event_colors().items():
        print(color)


if __name__ == '__main__':
    main()
