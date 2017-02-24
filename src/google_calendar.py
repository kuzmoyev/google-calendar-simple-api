import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


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

    def create_event(self, event):
        return self.service.events().insert(calendarId=self.calendar, body=event.get_body()).execute()

    def delete_event(self, event_id):
        return self.service.events().delete(calendarId=self.calendar, eventId=event_id).execute()

    def list_events(self):
        return self.service.events().list(calendarId=self.calendar).execute()['items']


def main():
    calendar = GoogleCalendar('kuzmovich.goog@gmail.com')
    print(calendar.list_events())


if __name__ == '__main__':
    main()
