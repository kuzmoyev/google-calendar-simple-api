from unittest import TestCase
from beautiful_date import Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sept, Oct, Dec, hours, days, Nov

from gcsa.attachment import Attachment
from gcsa.attendee import Attendee, ResponseStatus
from gcsa.conference import ConferenceSolution, EntryPoint, SolutionType, ConferenceSolutionCreateRequest
from gcsa.event import Event, Visibility
from gcsa.recurrence import Recurrence, DAILY, SU, SA, MONDAY, WEEKLY
from gcsa.reminders import PopupReminder, EmailReminder
from gcsa.serializers.event_serializer import EventSerializer
from gcsa.util.date_time_util import ensure_localisation

TEST_TIMEZONE = 'Pacific/Fiji'


class TestEvent(TestCase):
    def test_init(self):
        event = Event(
            'Breakfast',
            event_id='123',
            start=(1 / Feb / 2019)[9:00],
            end=(31 / Dec / 2019)[23:59],
            _created=ensure_localisation((20 / Nov / 2020)[16:19], TEST_TIMEZONE),
            _updated=ensure_localisation((25 / Nov / 2020)[16:19], TEST_TIMEZONE),
            timezone=TEST_TIMEZONE,
            description='Everyday breakfast',
            location='Home',
            guests_can_invite_others=False,
            guests_can_modify=True,
            guests_can_see_other_guests=False,
            recurrence=[
                Recurrence.rule(freq=DAILY),
                Recurrence.exclude_rule(by_week_day=[SU, SA]),
                Recurrence.exclude_dates([
                    19 / Apr / 2019,
                    22 / Apr / 2019,
                    12 / May / 2019
                ])
            ],
            visibility=Visibility.PRIVATE,
            minutes_before_popup_reminder=15
        )

        self.assertEqual(event.summary, 'Breakfast')
        self.assertEqual(event.id, '123')
        self.assertEqual(event.start, ensure_localisation((1 / Feb / 2019)[9:00], TEST_TIMEZONE))
        self.assertEqual(event.end, ensure_localisation((31 / Dec / 2019)[23:59], TEST_TIMEZONE))
        self.assertEqual(event.created, ensure_localisation((20 / Nov / 2020)[16:19], TEST_TIMEZONE))
        self.assertEqual(event.updated, ensure_localisation((25 / Nov / 2020)[16:19], TEST_TIMEZONE))
        self.assertEqual(event.description, 'Everyday breakfast')
        self.assertEqual(event.location, 'Home')
        self.assertEqual(len(event.recurrence), 3)
        self.assertEqual(event.visibility, Visibility.PRIVATE)
        self.assertIsInstance(event.reminders[0], PopupReminder)
        self.assertEqual(event.reminders[0].minutes_before_start, 15)
        self.assertFalse(event.guests_can_invite_others)
        self.assertTrue(event.guests_can_modify)
        self.assertFalse(event.guests_can_see_other_guests)

    def test_init_no_end(self):
        start = 1 / Jun / 2019
        event = Event('Good day', start, timezone=TEST_TIMEZONE)
        self.assertEqual(event.end, start + 1 * days)

        start = ensure_localisation((1 / Jul / 2019)[12:00], TEST_TIMEZONE)
        event = Event('Lunch', start, timezone=TEST_TIMEZONE)
        self.assertEqual(event.end, start + 1 * hours)

    def test_init_no_start_or_end(self):
        event = Event('Good day', start=None, timezone=TEST_TIMEZONE)
        self.assertIsNone(event.start)
        self.assertIsNone(event.end)

    def test_init_different_date_types(self):
        with self.assertRaises(TypeError):
            Event('Good day', start=(1 / Jan / 2019), end=(2 / Jan / 2019)[5:55], timezone=TEST_TIMEZONE)

    def test_add_attachment(self):
        e = Event('Good day', start=(1 / Aug / 2019), timezone=TEST_TIMEZONE)
        e.add_attachment('https://file.url', 'My file', "application/vnd.google-apps.document")

        self.assertIsInstance(e.attachments[0], Attachment)
        self.assertEqual(e.attachments[0].title, 'My file')

    def test_add_reminders(self):
        e = Event('Good day', start=(28 / Mar / 2019), timezone=TEST_TIMEZONE)

        self.assertEqual(len(e.reminders), 0)

        e.add_email_reminder(35)
        self.assertEqual(len(e.reminders), 1)
        self.assertIsInstance(e.reminders[0], EmailReminder)
        self.assertEqual(e.reminders[0].minutes_before_start, 35)

        e.add_popup_reminder(41)
        self.assertEqual(len(e.reminders), 2)
        self.assertIsInstance(e.reminders[1], PopupReminder)
        self.assertEqual(e.reminders[1].minutes_before_start, 41)

    def test_add_attendees(self):
        e = Event('Good day',
                  start=(17 / Jul / 2020),
                  timezone=TEST_TIMEZONE,
                  attendees=[
                      Attendee(email="attendee@gmail.com"),
                      "attendee2@gmail.com",
                  ])

        self.assertEqual(len(e.attendees), 2)
        e.add_attendee(Attendee("attendee3@gmail.com"))
        e.add_attendee(Attendee(email="attendee4@gmail.com"))
        self.assertEqual(len(e.attendees), 4)

        self.assertEqual(e.attendees[0].email, "attendee@gmail.com")
        self.assertEqual(e.attendees[1].email, "attendee2@gmail.com")
        self.assertEqual(e.attendees[2].email, "attendee3@gmail.com")
        self.assertEqual(e.attendees[3].email, "attendee4@gmail.com")

    def test_reminders_checks(self):
        with self.assertRaises(ValueError):
            Event('Too many reminders',
                  start=20 / Jul / 2020,
                  reminders=[EmailReminder()] * 6)

        with self.assertRaises(ValueError):
            Event('Default and overrides together',
                  start=20 / Jul / 2020,
                  reminders=EmailReminder(),
                  default_reminders=True)

        e = Event('Almost too many reminders',
                  start=20 / Jul / 2020,
                  reminders=[EmailReminder()] * 5)
        with self.assertRaises(ValueError):
            e.add_email_reminder()

    def test_repr_str(self):
        e = Event('Good event',
                  start=20 / Jul / 2020)
        self.assertEqual(str(e), '2020-07-20 - Good event')

        self.assertEqual(repr(e), '<Event 2020-07-20 - Good event>')

    def test_equal(self):
        dp = {
            'summary': 'Breakfast',
            'start': (1 / Feb / 2019)[9:00]
        }

        attachments_dp = {
            "file_url": 'https://file.com',
            "mime_type": "application/vnd.google-apps.map"
        }

        event1 = Event(
            **dp,
            event_id='123',
            end=(31 / Dec / 2019)[23:59],
            timezone=TEST_TIMEZONE,
            description='Everyday breakfast',
            location='Home',
            recurrence=Recurrence.rule(freq=DAILY),
            color_id='1',
            visibility=Visibility.PRIVATE,
            attendees='mail@gmail.com',
            attachments=Attachment(title='My doc', **attachments_dp),
            minutes_before_popup_reminder=15,
            other={"key": "value"}
        )

        self.assertEqual(event1, event1)
        self.assertNotEqual(Event(**dp), Event('Breakfast', start=(22 / Jun / 2020)[22:22]))

        self.assertNotEqual(Event(**dp, event_id='123'),
                            Event(**dp, event_id='abc'))

        self.assertNotEqual(Event(**dp, description='Desc1'),
                            Event(**dp, description='Desc2'))

        self.assertNotEqual(Event(**dp, location='Home'),
                            Event(**dp, location='Work'))

        self.assertNotEqual(Event(**dp, recurrence=Recurrence.rule(freq=DAILY)),
                            Event(**dp, recurrence=Recurrence.rule(freq=WEEKLY)))

        self.assertNotEqual(Event(**dp, color_id='1'),
                            Event(**dp, color_id='2'))

        self.assertNotEqual(Event(**dp, visibility=Visibility.PRIVATE),
                            Event(**dp, visibility=Visibility.PUBLIC))

        self.assertNotEqual(Event(**dp, attendees='mail1@gmail.com'),
                            Event(**dp, attendees='mail2@gmail.com'))

        self.assertNotEqual(Event(**dp, attachments=Attachment(title='Attachment1', **attachments_dp)),
                            Event(**dp, attachments=Attachment(title='Attachment2', **attachments_dp)))

        self.assertNotEqual(Event(**dp, minutes_before_email_reminder=10),
                            Event(**dp, minutes_before_popup_reminder=10))

        self.assertNotEqual(Event(**dp, other={"key1": "value1"}),
                            Event(**dp, other={"key2": "value2"}))

    def test_ordering(self):
        e1 = Event('Good day', start=(28 / Sept / 2020), end=(30 / Sept / 2020), timezone=TEST_TIMEZONE)
        e2 = Event('Good day', start=(28 / Sept / 2020), end=(16 / Oct / 2020), timezone=TEST_TIMEZONE)
        e3 = Event('Good day', start=(29 / Sept / 2020), end=(30 / Sept / 2020), timezone=TEST_TIMEZONE)
        e4 = Event('Good day', start=(29 / Sept / 2020)[22:22], end=(30 / Sept / 2020)[15:15], timezone=TEST_TIMEZONE)
        e5 = Event('Good day', start=(29 / Sept / 2020)[22:22], end=(30 / Sept / 2020)[18:15], timezone=TEST_TIMEZONE)
        e6 = Event('Good day', start=(29 / Sept / 2020)[23:22], end=(30 / Sept / 2020)[18:15], timezone=TEST_TIMEZONE)

        self.assertEqual(list(sorted([e5, e6, e1, e3, e2, e4])), [e1, e2, e3, e4, e5, e6])

        self.assertTrue(e1 < e2)
        self.assertTrue(e3 > e2)
        self.assertTrue(e5 >= e2)
        self.assertTrue(e2 >= e2)
        self.assertTrue(e5 <= e5)
        self.assertTrue(e5 <= e6)


class TestEventSerializer(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_to_json(self):
        e = Event('Good day', start=(28 / Sept / 2019), timezone=TEST_TIMEZONE)
        expected_event_json = {
            'summary': 'Good day',
            'start': {'date': '2019-09-28'},
            'end': {'date': '2019-09-29'},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

        e = Event('Good day', start=(28 / Oct / 2019)[11:22:33], timezone=TEST_TIMEZONE)
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-10-28T11:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-10-28T12:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_recurrence(self):
        e = Event('Good day',
                  start=(1 / Jan / 2019)[11:22:33],
                  end=(1 / Jan / 2020)[11:22:33],
                  timezone=TEST_TIMEZONE,
                  recurrence=[
                      Recurrence.rule(freq=DAILY),
                      Recurrence.exclude_rule(by_week_day=MONDAY),
                      Recurrence.exclude_dates([
                          19 / Apr / 2019,
                          22 / Apr / 2019,
                          12 / May / 2019
                      ])
                  ])
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2020-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [
                'RRULE:FREQ=DAILY;WKST=SU',
                'EXRULE:FREQ=DAILY;BYDAY=MO;WKST=SU',
                'EXDATE;VALUE=DATE:20190419,20190422,20190512'
            ],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_attachments(self):
        e = Event('Good day',
                  start=(1 / Jan / 2019)[11:22:33],
                  timezone=TEST_TIMEZONE,
                  attachments=[
                      Attachment('https://file.url1', 'My file1', "application/vnd.google-apps.document"),
                      Attachment('https://file.url2', 'My file2', "application/vnd.google-apps.document")
                  ])
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [
                {
                    'title': 'My file1',
                    'fileUrl': 'https://file.url1',
                    'mimeType': 'application/vnd.google-apps.document'
                },
                {
                    'title': 'My file2',
                    'fileUrl': 'https://file.url2',
                    'mimeType': 'application/vnd.google-apps.document'
                }
            ],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_reminders(self):
        e = Event('Good day',
                  start=(1 / Jan / 2019)[11:22:33],
                  timezone=TEST_TIMEZONE,
                  minutes_before_popup_reminder=30,
                  minutes_before_email_reminder=120)
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                    {'method': 'email', 'minutes': 120}
                ],
                'useDefault': False
            },
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_attendees(self):
        e = Event('Good day',
                  start=(1 / Jul / 2020)[11:22:33],
                  timezone=TEST_TIMEZONE,
                  attendees=[
                      Attendee(email='attendee@gmail.com', _response_status=ResponseStatus.NEEDS_ACTION),
                      Attendee(email='attendee2@gmail.com', _response_status=ResponseStatus.ACCEPTED),
                  ])
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2020-07-01T11:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2020-07-01T12:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [
                {'email': 'attendee@gmail.com', 'responseStatus': ResponseStatus.NEEDS_ACTION},
                {'email': 'attendee2@gmail.com', 'responseStatus': ResponseStatus.ACCEPTED},
            ],
            'reminders': {'useDefault': False},
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

        e = Event('Good day2',
                  start=20 / Jul / 2020,
                  default_reminders=True)
        expected_event_json = {
            'summary': 'Good day2',
            'start': {'date': '2020-07-20'},
            'end': {'date': '2020-07-21'},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': True},
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_conference_solution(self):
        e = Event(
            'Good day',
            start=(1 / Jul / 2020)[11:22:33],
            timezone=TEST_TIMEZONE,
            conference_solution=ConferenceSolution(
                entry_points=EntryPoint(EntryPoint.VIDEO, uri='https://video.com'),
                solution_type=SolutionType.HANGOUTS_MEET,
                name='Hangout',
                icon_uri='https://icon.com',
                conference_id='aaa-bbbb-ccc',
                signature='abc4efg12345',
                notes='important notes'
            )
        )
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2020-07-01T11:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2020-07-01T12:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [],
            'conferenceData': {
                'entryPoints': [
                    {
                        'entryPointType': 'video',
                        'uri': 'https://video.com',
                    }
                ],
                'conferenceSolution': {
                    'key': {
                        'type': 'hangoutsMeet'
                    },
                    'name': 'Hangout',
                    'iconUri': 'https://icon.com'
                },
                'conferenceId': 'aaa-bbbb-ccc',
                'signature': 'abc4efg12345',
                'notes': 'important notes'
            },
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_conference_solution_create_request(self):
        e = Event(
            'Good day',
            start=(1 / Jul / 2020)[11:22:33],
            timezone=TEST_TIMEZONE,
            conference_solution=ConferenceSolutionCreateRequest(
                solution_type=SolutionType.HANGOUTS_MEET,
                request_id='hello1234',
                conference_id='conference-id',
                signature='signature',
                notes='important notes',
                _status='pending'
            )
        )
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2020-07-01T11:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2020-07-01T12:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [],
            'conferenceData': {
                'createRequest': {
                    'requestId': 'hello1234',
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                    'status': {
                        'statusCode': 'pending'
                    }
                },
                'conferenceId': 'conference-id',
                'signature': 'signature',
                'notes': 'important notes'
            },
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_json_updated(self):
        e = Event(
            'Good day',
            start=(1 / Jul / 2020)[11:22:33],
            timezone=TEST_TIMEZONE,
            _updated=ensure_localisation((25 / Nov / 2020)[11:22:33], timezone=TEST_TIMEZONE)
        )
        expected_event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2020-07-01T11:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2020-07-01T12:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'attendees': [],
            'reminders': {'useDefault': False},
            'attachments': [],
            'guestsCanInviteOthers': True,
            'guestsCanModify': False,
            'guestsCanSeeOtherGuests': True,
        }
        self.assertDictEqual(EventSerializer.to_json(e), expected_event_json)

    def test_to_object(self):
        event_json = {
            'summary': 'Good day',
            'description': 'Very good day indeed',
            'location': 'Prague',
            'start': {'dateTime': '2019-01-01T11:22:33', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33', 'timeZone': TEST_TIMEZONE},
            'updated': '2020-11-25T14:53:46.0Z',
            'created': '2020-11-24T14:53:46.0Z',
            'recurrence': [
                'RRULE:FREQ=DAILY;WKST=SU',
                'EXRULE:FREQ=DAILY;BYDAY=MO;WKST=SU',
                'EXDATE:VALUE=DATE:20190419,20190422,20190512'
            ],
            'visibility': 'public',
            'attendees': [
                {'email': 'attendee@gmail.com', 'responseStatus': ResponseStatus.NEEDS_ACTION},
                {'email': 'attendee2@gmail.com', 'responseStatus': ResponseStatus.ACCEPTED},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                    {'method': 'email', 'minutes': 120}
                ]
            },
            'attachments': [
                {
                    'title': 'My file1',
                    'fileUrl': 'https://file.url1',
                    'mimeType': 'application/vnd.google-apps.document'
                },
                {
                    'title': 'My file2',
                    'fileUrl': 'https://file.url2',
                    'mimeType': 'application/vnd.google-apps.document'
                }
            ],
            'conferenceData': {
                'entryPoints': [
                    {
                        'entryPointType': 'video',
                        'uri': 'https://video.com',
                    }
                ],
                'conferenceSolution': {
                    'key': {
                        'type': 'hangoutsMeet'
                    },
                    'name': 'Hangout',
                    'iconUri': 'https://icon.com'
                },
                'conferenceId': 'aaa-bbbb-ccc',
                'signature': 'abc4efg12345',
                'notes': 'important notes'
            },
            'guestsCanInviteOthers': False,
            'guestsCanModify': True,
            'guestsCanSeeOtherGuests': False,
            'transparency': 'transparent',
            'creator': {
                'id': '123123',
                'email': 'creator@gmail.com',
                'displayName': 'Creator',
                'self': True
            },
            'organizer': {
                'id': '456456',
                'email': 'organizer@gmail.com',
                'displayName': 'Organizer',
                'self': False
            }
        }

        serializer = EventSerializer(event_json)
        event = serializer.get_object()

        self.assertEqual(event.summary, 'Good day')
        self.assertEqual(event.start, ensure_localisation((1 / Jan / 2019)[11:22:33], TEST_TIMEZONE))
        self.assertEqual(event.end, ensure_localisation((1 / Jan / 2019)[12:22:33], TEST_TIMEZONE))
        self.assertEqual(event.updated, ensure_localisation((25 / Nov / 2020)[14:53:46], 'UTC'))
        self.assertEqual(event.created, ensure_localisation((24 / Nov / 2020)[14:53:46], 'UTC'))
        self.assertEqual(event.description, 'Very good day indeed')
        self.assertEqual(event.location, 'Prague')
        self.assertEqual(len(event.recurrence), 3)
        self.assertEqual(event.visibility, Visibility.PUBLIC)
        self.assertEqual(len(event.attendees), 2)
        self.assertIsInstance(event.reminders[0], PopupReminder)
        self.assertEqual(event.reminders[0].minutes_before_start, 30)
        self.assertIsInstance(event.reminders[1], EmailReminder)
        self.assertEqual(event.reminders[1].minutes_before_start, 120)
        self.assertEqual(len(event.attachments), 2)
        self.assertIsInstance(event.attachments[0], Attachment)
        self.assertEqual(event.attachments[0].title, 'My file1')
        self.assertIsInstance(event.conference_solution, ConferenceSolution)
        self.assertEqual(event.conference_solution.solution_type, 'hangoutsMeet')
        self.assertEqual(event.conference_solution.entry_points[0].uri, 'https://video.com')
        self.assertFalse(event.guests_can_invite_others)
        self.assertTrue(event.guests_can_modify)
        self.assertFalse(event.guests_can_see_other_guests)
        self.assertEqual(event.transparency, 'transparent')
        self.assertEqual(event.creator.email, 'creator@gmail.com')
        self.assertEqual(event.organizer.email, 'organizer@gmail.com')

        event_json_str = """{
            "summary": "Good day",
            "description": "Very good day indeed",
            "location": "Prague",
            "start": {"date": "2020-07-20"},
            "end": {"date": "2020-07-22"}
        }"""

        event = EventSerializer.to_object(event_json_str)

        self.assertEqual(event.summary, 'Good day')
        self.assertEqual(event.description, 'Very good day indeed')
        self.assertEqual(event.location, 'Prague')
        self.assertEqual(event.start, 20 / Jul / 2020)
        self.assertEqual(event.end, 22 / Jul / 2020)

    def test_to_object_recurring_event(self):
        event_json_str = {
            "id": 'recurring_event_id_20201107T070000Z',
            "summary": "Good day",
            "description": "Very good day indeed",
            "location": "Prague",
            "start": {"date": "2020-07-20"},
            "end": {"date": "2020-07-22"},
            "recurringEventId": 'recurring_event_id'
        }

        event = EventSerializer.to_object(event_json_str)

        self.assertEqual(event.id, 'recurring_event_id_20201107T070000Z')
        self.assertTrue(event.is_recurring_instance)
        self.assertEqual(event.recurring_event_id, 'recurring_event_id')

    def test_to_object_conference_data(self):
        event_json = {
            'summary': 'Good day',
            'description': 'Very good day indeed',
            'location': 'Prague',
            'start': {'dateTime': '2019-01-01T11:22:33', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33', 'timeZone': TEST_TIMEZONE},
            'conferenceData': {
                'createRequest': {
                    'requestId': 'hello1234',
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                    'status': {
                        'statusCode': 'pending'
                    }
                },
                'conferenceId': 'conference-id',
                'signature': 'signature',
                'notes': 'important notes'
            }
        }

        event = EventSerializer.to_object(event_json)
        self.assertIsInstance(event.conference_solution, ConferenceSolutionCreateRequest)
        self.assertEqual(event.conference_solution.solution_type, 'hangoutsMeet')

        # with successful conference create request
        event_json = {
            'summary': 'Good day',
            'description': 'Very good day indeed',
            'location': 'Prague',
            'start': {'dateTime': '2019-01-01T11:22:33', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33', 'timeZone': TEST_TIMEZONE},
            'conferenceData': {
                'entryPoints': [
                    {
                        'entryPointType': 'video',
                        'uri': 'https://video.com',
                    }
                ],
                'conferenceSolution': {
                    'key': {
                        'type': 'hangoutsMeet'
                    },
                    'name': 'Hangout',
                    'iconUri': 'https://icon.com'
                },
                'createRequest': {
                    'requestId': 'hello1234',
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                    'status': {
                        'statusCode': 'success'
                    }
                },
                'conferenceId': 'conference-id',
                'signature': 'signature',
                'notes': 'important notes'
            }
        }

        event = EventSerializer.to_object(event_json)
        self.assertIsInstance(event.conference_solution, ConferenceSolution)
        self.assertEqual(event.conference_solution.solution_type, 'hangoutsMeet')
        self.assertEqual(event.conference_solution.entry_points[0].uri, 'https://video.com')
