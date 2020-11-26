import pickle
from os import path
from unittest.mock import patch

import dateutil
from beautiful_date import D, days, years
from pyfakefs.fake_filesystem_unittest import TestCase

from gcsa.attendee import Attendee
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.serializers.event_serializer import EventSerializer
from gcsa.util.date_time_util import insure_localisation


class MockToken:
    def __init__(self, valid, refresh_token='refresh_token'):
        self.valid = valid
        self.expired = not valid
        self.refresh_token = refresh_token

    def refresh(self, _):
        self.valid = True
        self.expired = False


class TestGoogleCalendarCredentials(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        self.credentials_dir = '/.credentials'
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

        class MockAuthFlow:
            def run_local_server(self):
                return MockToken(valid=True)

        self.from_client_secrets_file = patch(
            'google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file',
            return_value=MockAuthFlow()
        ).start()

    def tearDown(self):
        self.build_patcher.stop()
        self.from_client_secrets_file.stop()

    def test_get_default_credentials_path_exist(self):
        self.fs.create_dir(path.join(path.expanduser('~'), '.credentials'))
        self.assertEqual(
            path.join(path.expanduser('~'), '.credentials/credentials.json'),
            GoogleCalendar._get_default_credentials_path()
        )

    def test_get_default_credentials_path_not_exist(self):
        self.assertFalse(path.exists(path.join(path.expanduser('~'), '.credentials')))
        self.assertEqual(
            path.join(path.expanduser('~'), '.credentials/credentials.json'),
            GoogleCalendar._get_default_credentials_path()
        )
        self.assertTrue(path.exists(path.join(path.expanduser('~'), '.credentials')))

    def test_get_token_valid(self):
        gc = GoogleCalendar(token_path=self.valid_token_path)
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(self.from_client_secrets_file.called)

    def test_get_token_expired(self):
        gc = GoogleCalendar(token_path=self.expired_token_path)
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(gc.credentials.expired)
        self.assertFalse(self.from_client_secrets_file.called)

    def test_get_token_invalid_refresh(self):
        gc = GoogleCalendar(credentials_path=self.credentials_path)
        self.assertTrue(gc.credentials.valid)
        self.assertFalse(gc.credentials.expired)
        self.assertTrue(self.from_client_secrets_file.called)


def executable(fn):
    """Decorator that stores data received from the function in object that returns that data when
    called its `execute` method. Emulates HttpRequest from googleapiclient."""

    class Executable:
        def __init__(self, data):
            self.data = data

        def execute(self):
            return self.data

    def wrapper(*args, **kwargs):
        data = fn(*args, **kwargs)
        return Executable(data)

    return wrapper


class MockEventsRequests:
    """Emulates GoogleCalendar.service.events()"""

    EVENTS_PER_PAGE = 3

    @executable
    def instances(self, **kwargs):
        event_id = kwargs.pop('eventId')

        if event_id == 'event_id_1':
            recurring_instances = [
                Event(
                    'Recurring event 1',
                    start=D.now() + 1 * days,
                    event_id='event_id_1_' + (D.now() + (i + 1) * days).isoformat() + 'Z',
                    _updated=D.now() + 5 * days,
                    _recurring_event_id='event_id_1',

                ) for i in range(1, 10)
            ]
        elif event_id == 'event_id_2':
            recurring_instances = [
                Event(
                    'Recurring event 2',
                    start=D.now() + 2 * days,
                    event_id='event_id_2_' + (D.now() + (i + 2) * days).isoformat() + 'Z',
                    _updated=D.now() + 5 * days,
                    _recurring_event_id='event_id_2',

                ) for i in range(1, 5)
            ]
        else:
            # should get here in tests
            raise ValueError

        return {
            'items': recurring_instances,
            'nextPageToken': None
        }

    @executable
    def list(self, **kwargs):
        """Emulates GoogleCalendar.service.events().list().execute()"""

        time_min = dateutil.parser.parse(kwargs['timeMin'])
        time_max = dateutil.parser.parse(kwargs['timeMax'])
        order_by = kwargs['orderBy']
        single_events = kwargs['singleEvents']
        page_token = kwargs['pageToken'] or 0  # page number in this case
        q = kwargs['q']

        test_events = [
            Event(
                'test{}'.format(i),
                start=insure_localisation(D.now() + i * days),
                event_id='1',
                _updated=insure_localisation(D.now() + (i + 1) * days),
                attendees=[
                    Attendee(email='{}@gmail.com'.format(attendee_name.lower()), display_name=attendee_name)
                ] if attendee_name else None
            )
            for i, attendee_name in zip(range(1, 10), ['John', 'Josh'] + [''] * 8)
        ]

        recurring_event = Event('Recurring event',
                                start=D.now() + 9 * days,
                                event_id='recurring_id',
                                _updated=insure_localisation(D.now() + 10 * days))
        recurring_instances = [
            Event(
                recurring_event.summary,
                start=recurring_event.start + i * days,
                event_id=recurring_event.id + '_' + (recurring_event.start + i * days).isoformat() + 'Z',
                _updated=recurring_event.updated,
                _recurring_event_id=recurring_event.id,

            ) for i in range(10)
        ]

        if single_events:
            test_events.extend(recurring_instances)
        else:
            test_events.append(recurring_event)

        event_in_a_year = Event(
            'test42',
            start=insure_localisation(D.now() + 1 * years + 1 * days),
            event_id='42',
            _updated=insure_localisation(D.now() + 1 * years + 2 * days),
            attendees=[
                Attendee(email='frank@gmail.com', display_name='Frank')
            ]
        )
        test_events.append(event_in_a_year)

        def _filter(e):
            return (
                    (time_min <= e.start and e.end < time_max) and
                    (
                            not q or
                            q in e.summary or
                            (e.description and q in e.description) or
                            (e.attendees and any((a.display_name and q in a.display_name) for a in e.attendees))
                    )
            )

        def _sort_key(e):
            if order_by is None:
                return e.id
            if order_by == 'startTime':
                return e.start
            if order_by == 'updated':
                return e.updated

        filtered_events = list(filter(_filter, test_events))
        ordered_events = sorted(filtered_events, key=_sort_key)
        serialized_events = list(map(self._serialize_event, ordered_events))

        current_page_events = ordered_events[page_token * self.EVENTS_PER_PAGE:(page_token + 1) * self.EVENTS_PER_PAGE]
        return {
            'items': current_page_events,
            'nextPageToken': page_token + 1 if (page_token + 1) * 3 < len(serialized_events) else None
        }

    @staticmethod
    def _serialize_event(e):
        event_json = EventSerializer.to_json(e)
        event_json['updated'] = e.updated.isoformat() + 'Z'
        return event_json


class MockService:
    @staticmethod
    def events():
        return MockEventsRequests()


class TestGoogleCalendarAPI(TestCase):
    def setUp(self):
        self.build_patcher = patch('googleapiclient.discovery.build', return_value=MockService())
        self.build_patcher.start()
        self.get_credentials_patcher = patch('gcsa.google_calendar.GoogleCalendar._get_default_credentials_path',
                                             return_value='/')
        self.get_credentials_patcher.start()
        self.get_token_patcher = patch('gcsa.google_calendar.GoogleCalendar._get_token')
        self.get_token_patcher.start()

        self.gc = GoogleCalendar()

    def tearDown(self):
        self.build_patcher.stop()
        self.get_credentials_patcher.stop()
        self.get_token_patcher.stop()

    def test_get_events_default(self):
        events = list(self.gc.get_events())
        self.assertEqual(len(events), 10)
        self.assertFalse(any(e.is_recurring_instance for e in events))

        events = list(self.gc)
        self.assertEqual(len(events), 10)
        self.assertFalse(any(e.is_recurring_instance for e in events))

    def test_get_events_time_limits(self):
        time_min = insure_localisation(D.now() + 5 * days)
        events = list(self.gc.get_events(time_min=time_min))
        self.assertEqual(len(events), 7)
        self.assertTrue(all(e.start >= time_min for e in events))

        time_min = insure_localisation(D.now() + 5 * days)
        events = list(self.gc[time_min])
        self.assertEqual(len(events), 7)
        self.assertTrue(all(e.start >= time_min for e in events))

        time_max = insure_localisation(D.now() + 1 * years + 7 * days)
        events = list(self.gc.get_events(time_max=time_max))
        self.assertEqual(len(events), 11)
        self.assertTrue(all(e.end < time_max for e in events))

        time_max = insure_localisation(D.now() + 7 * days)
        events = list(self.gc.get_events(time_max=time_max))
        self.assertEqual(len(events), 6)
        self.assertTrue(all(e.end < time_max for e in events))

        events = list(self.gc.get_events(time_min=time_min, time_max=time_max))
        self.assertEqual(len(events), 2)
        self.assertTrue(all(time_min <= e.start and e.end < time_max for e in events))

        events = list(self.gc[time_min:time_max])
        self.assertEqual(len(events), 2)
        self.assertTrue(all(time_min <= e.start and e.end < time_max for e in events))

        time_min = D.today() + 5 * days
        time_max = D.today() + 7 * days
        events = list(self.gc.get_events(time_min=time_min, time_max=time_max))
        self.assertEqual(len(events), 3)

        time_min = insure_localisation(time_min[0:0])
        time_max = insure_localisation(time_max[23:59:59])
        self.assertTrue(all(time_min <= e.start and e.end < time_max for e in events))

        with self.assertRaises(NotImplementedError):
            _ = self.gc[5]
        with self.assertRaises(ValueError):
            _ = self.gc[5:10]

    def test_get_events_single_events(self):
        events = list(self.gc.get_events(single_events=True))
        self.assertEqual(len(events), 19)
        self.assertTrue(all(e.is_recurring_instance for e in events if e.summary == 'Recurring event'))

        events = list(self.gc.get_events(single_events=False))
        self.assertEqual(len(events), 10)
        self.assertTrue(all(not e.is_recurring_instance for e in events if e.summary == 'Recurring event'))

        with self.assertRaises(ValueError):
            # can only be used with single events
            list(self.gc.get_events(order_by='startTime'))

    def test_get_events_order_by(self):
        events = list(self.gc.get_events(order_by='updated'))
        self.assertEqual(len(events), 10)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.updated).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.updated).id)

        events = list(self.gc[::'updated'])
        self.assertEqual(len(events), 10)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.updated).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.updated).id)

        events = list(self.gc[::'startTime'])
        self.assertEqual(len(events), 19)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.start).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.start).id)

        events = list(self.gc.get_events(order_by='startTime', single_events=True))
        self.assertEqual(len(events), 19)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.start).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.start).id)

    def test_get_events_query(self):
        events = list(self.gc.get_events(query='test4', time_max=D.now() + 2 * years))
        self.assertEqual(len(events), 2)  # test4 and test42

        events = list(self.gc.get_events(query='Jo', time_max=D.now() + 2 * years))
        self.assertEqual(len(events), 2)  # with John and Josh

        events = list(self.gc.get_events(query='Josh', time_max=D.now() + 2 * years))
        self.assertEqual(len(events), 1)

        events = list(self.gc.get_events(query='Frank', time_max=D.now() + 2 * years))
        self.assertEqual(len(events), 1)

    def test_get_recurring_instances(self):
        events = list(self.gc.get_instances(recurring_event='event_id_1'))
        self.assertEqual(len(events), 9)
        self.assertTrue(all(e.id.startswith('event_id_1') for e in events))

        recurring_event = Event(
            'recurring event',
            D.now(),
            event_id='event_id_2'
        )
        events = list(self.gc.get_instances(recurring_event=recurring_event))
        self.assertEqual(len(events), 4)
        self.assertTrue(all(e.id.startswith('event_id_2') for e in events))
