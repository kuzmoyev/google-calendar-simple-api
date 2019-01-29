from unittest import TestCase
from beautiful_date import Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sept, Oct, Dec, hours, days

from gcsa.attachment import Attachment
from gcsa.event import Event, Visibility
from gcsa.recurrence import Recurrence, DAILY, SU, SA, MONDAY
from gcsa.reminders import PopupReminder, EmailReminder
from gcsa.serializers.event_serializer import EventSerializer
from util.date_time_util import insure_localisation

TEST_TIMEZONE = 'Pacific/Fiji'


class TestEvent(TestCase):
    def test_init(self):
        event = Event(
            'Breakfast',
            start=(1 / Feb / 2019)[9:00],
            end=(31 / Dec / 2019)[23:59],
            timezone=TEST_TIMEZONE,
            description='Everyday breakfast',
            location='Home',
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
        self.assertEqual(event.start, insure_localisation((1 / Feb / 2019)[9:00], TEST_TIMEZONE))
        self.assertEqual(event.description, 'Everyday breakfast')
        self.assertEqual(event.location, 'Home')
        self.assertEqual(len(event.recurrence), 3)
        self.assertEqual(event.visibility, Visibility.PRIVATE)
        self.assertIsInstance(event.reminders[0], PopupReminder)
        self.assertEqual(event.reminders[0].minutes_before_start, 15)

    def test_init_no_end(self):
        start = 1 / Jun / 2019
        event = Event('Good day', start, timezone=TEST_TIMEZONE)
        self.assertEqual(event.end, start + 1 * days)

        start = insure_localisation((1 / Jul / 2019)[12:00], TEST_TIMEZONE)
        event = Event('Lunch', start, timezone=TEST_TIMEZONE)
        self.assertEqual(event.end, start + 1 * hours)

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


class TestEventSerializer(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_to_json(self):
        e = Event('Good day', start=(28 / Sept / 2019), timezone=TEST_TIMEZONE)
        event_json = {
            'summary': 'Good day',
            'start': {'date': '2019-09-28'},
            'end': {'date': '2019-09-29'},
            'recurrence': [],
            'visibility': 'default',
            'reminders': {'useDefault': False},
            'attachments': []
        }
        self.assertDictEqual(EventSerializer.to_json(e), event_json)

        e = Event('Good day', start=(28 / Oct / 2019)[11:22:33], timezone=TEST_TIMEZONE)
        event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-10-28T11:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-10-28T12:22:33+12:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'reminders': {'useDefault': False},
            'attachments': []
        }
        self.assertDictEqual(EventSerializer.to_json(e), event_json)

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
        event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2020-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [
                'RRULE:FREQ=DAILY;WKST=SU',
                'EXRULE:FREQ=DAILY;BYDAY=MO;WKST=SU',
                'EXDATE;VALUE=DATE:20190419,20190422,20190512'
            ],
            'visibility': 'default',
            'reminders': {'useDefault': False},
            'attachments': []
        }
        self.assertDictEqual(EventSerializer.to_json(e), event_json)

    def test_to_json_attachments(self):
        e = Event('Good day',
                  start=(1 / Jan / 2019)[11:22:33],
                  timezone=TEST_TIMEZONE,
                  attachments=[
                      Attachment('My file1', 'https://file.url1', "application/vnd.google-apps.document"),
                      Attachment('My file2', 'https://file.url2', "application/vnd.google-apps.document")
                  ])
        event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
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
            ]
        }
        self.assertDictEqual(EventSerializer.to_json(e), event_json)

    def test_to_json_reminders(self):
        e = Event('Good day',
                  start=(1 / Jan / 2019)[11:22:33],
                  timezone=TEST_TIMEZONE,
                  minutes_before_popup_reminder=30,
                  minutes_before_email_reminder=120)
        event_json = {
            'summary': 'Good day',
            'start': {'dateTime': '2019-01-01T11:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33+13:00', 'timeZone': TEST_TIMEZONE},
            'recurrence': [],
            'visibility': 'default',
            'reminders': {
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                    {'method': 'email', 'minutes': 120}
                ],
                'useDefault': False
            },
            'attachments': []
        }
        self.assertDictEqual(EventSerializer.to_json(e), event_json)

    def test_to_object(self):
        event_json = {
            'summary': 'Good day',
            'description': 'Very good day indeed',
            'location': 'Prague',
            'start': {'dateTime': '2019-01-01T11:22:33', 'timeZone': TEST_TIMEZONE},
            'end': {'dateTime': '2019-01-01T12:22:33', 'timeZone': TEST_TIMEZONE},
            'recurrence': [
                'RRULE:FREQ=DAILY;WKST=SU',
                'EXRULE:FREQ=DAILY;BYDAY=MO;WKST=SU',
                'EXDATE:VALUE=DATE:20190419,20190422,20190512'
            ],
            'visibility': 'public',
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
            ]
        }

        event = EventSerializer.to_object(event_json)

        self.assertEqual(event.summary, 'Good day')
        self.assertEqual(event.start, insure_localisation((1 / Jan / 2019)[11:22:33], TEST_TIMEZONE))
        self.assertEqual(event.end, insure_localisation((1 / Jan / 2019)[12:22:33], TEST_TIMEZONE))
        self.assertEqual(event.description, 'Very good day indeed')
        self.assertEqual(event.location, 'Prague')
        self.assertEqual(len(event.recurrence), 3)
        self.assertEqual(event.visibility, Visibility.PUBLIC)
        self.assertIsInstance(event.reminders[0], PopupReminder)
        self.assertEqual(event.reminders[0].minutes_before_start, 30)
        self.assertIsInstance(event.reminders[1], EmailReminder)
        self.assertEqual(event.reminders[1].minutes_before_start, 120)
        self.assertEqual(len(event.attachments), 2)
        self.assertIsInstance(event.attachments[0], Attachment)
        self.assertEqual(event.attachments[0].title, 'My file1')
