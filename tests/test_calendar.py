from unittest import TestCase

from gcsa.calendar import Calendar, CalendarListEntry, NotificationType, AccessRoles
from gcsa.conference import SolutionType
from gcsa.reminders import EmailReminder, PopupReminder
from gcsa.serializers.calendar_serializer import CalendarSerializer, CalendarListEntrySerializer

TEST_TIMEZONE = 'Pacific/Fiji'
TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES = [SolutionType.HANGOUT, SolutionType.NAMED_HANGOUT]
TEST_NOTIFICATION_TYPES = [NotificationType.EVENT_CREATION, NotificationType.EVENT_CHANGE]
TEST_ACCESS_ROLE = AccessRoles.OWNER


class TestCalendar(TestCase):
    def test_init(self):
        c = Calendar(
            summary='Summary',
            calendar_id='Calendar id',
            description='Description',
            location='Fiji',
            timezone=TEST_TIMEZONE,
            allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )

        self.assertEqual(c.summary, 'Summary')
        self.assertEqual(c.calendar_id, 'Calendar id')
        self.assertEqual(c.id, 'Calendar id')
        self.assertEqual(c.description, 'Description')
        self.assertEqual(c.location, 'Fiji')
        self.assertEqual(c.timezone, TEST_TIMEZONE)
        self.assertListEqual(c.allowed_conference_solution_types, TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES)

    def test_to_calendar_list_entry(self):
        c = Calendar(
            summary='Summary',
            calendar_id='Calendar id',
            description='Description',
            location='Fiji',
            timezone=TEST_TIMEZONE,
            allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )

        cle = c.to_calendar_list_entry(
            summary_override='Summary override',
            color_id='1',
            background_color='#123123',
            foreground_color='#234234',
            hidden=False,
            selected=True,
            default_reminders=[EmailReminder(60), PopupReminder(15)],
            notification_types=TEST_NOTIFICATION_TYPES
        )
        self.assertIsInstance(cle, CalendarListEntry)

        self.assertEqual(cle.summary_override, 'Summary override')
        self.assertEqual(cle.color_id, '1')
        self.assertEqual(cle.background_color, '#123123')
        self.assertEqual(cle.foreground_color, '#234234')
        self.assertFalse(cle.hidden)
        self.assertTrue(cle.selected)
        self.assertEqual(cle.default_reminders, [EmailReminder(60), PopupReminder(15)])
        self.assertEqual(cle.notification_types, TEST_NOTIFICATION_TYPES)

        c_without_id = Calendar(
            summary='Summary',
        )
        with self.assertRaises(ValueError):
            c_without_id.to_calendar_list_entry()

    def test_repr_str(self):
        c = Calendar(
            summary='Summary',
            calendar_id='Calendar id',
            description='Description'
        )
        self.assertEqual(str(c), 'Summary - Description')
        self.assertEqual(repr(c), '<Calendar Summary - Description>')

    def test_eq(self):
        c1 = Calendar(
            summary='Summary',
            calendar_id='Calendar id',
            description='Description',
            location='Fiji',
            timezone=TEST_TIMEZONE,
            allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )
        c2 = Calendar(
            summary='Summary2',
            calendar_id='Calendar id2',
            description='Description2',
            location='Fiji',
            timezone=TEST_TIMEZONE,
            allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )
        self.assertEqual(c1, c1)
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, 'Calendar')


class TestCalendarSerializer(TestCase):

    def test_to_json(self):
        c = Calendar(
            summary='Summary',
            calendar_id='Calendar id',
            description='Description',
            location='Fiji',
            timezone=TEST_TIMEZONE,
            allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )
        expected_calendar_json = {
            "id": 'Calendar id',
            "summary": 'Summary',
            "description": 'Description',
            "location": 'Fiji',
            "timeZone": TEST_TIMEZONE,
            "conferenceProperties": {
                "allowedConferenceSolutionTypes": TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
            }
        }
        self.assertDictEqual(CalendarSerializer.to_json(c), expected_calendar_json)

        c = Calendar(
            summary='Summary',
            description='Description',
            timezone=TEST_TIMEZONE
        )
        expected_calendar_json = {
            "summary": 'Summary',
            "description": 'Description',
            "timeZone": TEST_TIMEZONE
        }
        self.assertDictEqual(CalendarSerializer.to_json(c), expected_calendar_json)

    def test_to_object(self):
        calendar_json = {
            "id": 'Calendar id',
            "summary": 'Summary',
            "description": 'Description',
            "location": 'Fiji',
            "timeZone": TEST_TIMEZONE,
            "conferenceProperties": {
                "allowedConferenceSolutionTypes": TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
            }
        }

        serializer = CalendarSerializer(calendar_json)
        c = serializer.get_object()

        self.assertEqual(c.summary, 'Summary')
        self.assertEqual(c.calendar_id, 'Calendar id')
        self.assertEqual(c.description, 'Description')
        self.assertEqual(c.location, 'Fiji')
        self.assertEqual(c.timezone, TEST_TIMEZONE)
        self.assertListEqual(c.allowed_conference_solution_types, TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES)

        calendar_json = """{
            "id": "Calendar id",
            "summary": "Summary",
            "location": "Fiji"
        }"""

        serializer = CalendarSerializer(calendar_json)
        c = serializer.get_object()

        self.assertEqual(c.summary, 'Summary')
        self.assertEqual(c.calendar_id, 'Calendar id')
        self.assertIsNone(c.description)
        self.assertEqual(c.location, 'Fiji')
        self.assertIsNone(c.timezone)
        self.assertIsNone(c.allowed_conference_solution_types)


class TestCalendarListEntry(TestCase):
    def test_init(self):
        c = CalendarListEntry(
            summary_override='Summary override',
            color_id='1',
            background_color='#123123',
            foreground_color='#234234',
            hidden=False,
            selected=True,
            default_reminders=[EmailReminder(60), PopupReminder(15)],
            notification_types=TEST_NOTIFICATION_TYPES,
            _access_role=TEST_ACCESS_ROLE,
            _primary=True,
            _deleted=False,

            _summary='Summary',
            calendar_id='Calendar id',
            _description='Description',
            _location='Fiji',
            _timezone=TEST_TIMEZONE,
            _allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )

        self.assertEqual(c.summary_override, 'Summary override')
        self.assertEqual(c.color_id, '1')
        self.assertEqual(c.background_color, '#123123')
        self.assertEqual(c.foreground_color, '#234234')
        self.assertFalse(c.hidden)
        self.assertTrue(c.selected)
        self.assertEqual(c.default_reminders, [EmailReminder(60), PopupReminder(15)])
        self.assertEqual(c.notification_types, TEST_NOTIFICATION_TYPES)
        self.assertEqual(c.access_role, TEST_ACCESS_ROLE)
        self.assertTrue(c.primary)
        self.assertFalse(c.deleted)

        self.assertEqual(c.summary, 'Summary')
        self.assertEqual(c.calendar_id, 'Calendar id')
        self.assertEqual(c.description, 'Description')
        self.assertEqual(c.location, 'Fiji')
        self.assertEqual(c.timezone, TEST_TIMEZONE)
        self.assertListEqual(c.allowed_conference_solution_types, TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES)

        c.color_id = '2'
        self.assertEqual(c.color_id, '2')
        self.assertIsNone(c.background_color)
        self.assertIsNone(c.foreground_color)

    def test_repr_str(self):
        c = CalendarListEntry(
            calendar_id='Calendar id',
            summary_override='Summary override',
            _summary='Summary',
        )
        self.assertEqual(str(c), 'Summary override - (Summary)')
        self.assertEqual(repr(c), '<CalendarListEntry Summary override - (Summary)>')

    def test_eq(self):
        c1 = CalendarListEntry(
            calendar_id='Calendar id',
            summary_override='Summary override',
            _summary='Summary',
        )
        c2 = CalendarListEntry(
            calendar_id='Calendar id2',
            summary_override='Summary override2',
            _summary='Summary2',
        )
        self.assertEqual(c1, c1)
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, 'Calendar')


class TestCalendarListEntrySerializer(TestCase):

    def test_to_json(self):
        c = CalendarListEntry(
            summary_override='Summary override',
            color_id='1',
            background_color='#123123',
            foreground_color='#234234',
            hidden=False,
            selected=True,
            default_reminders=[EmailReminder(60), PopupReminder(15)],
            notification_types=TEST_NOTIFICATION_TYPES,
            _access_role=TEST_ACCESS_ROLE,
            _primary=True,
            _deleted=False,

            _summary='Summary',
            calendar_id='Calendar id',
            _description='Description',
            _location='Fiji',
            _timezone=TEST_TIMEZONE,
            _allowed_conference_solution_types=TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
        )
        expected_calendar_json = {
            'id': 'Calendar id',
            'summaryOverride': 'Summary override',
            'colorId': '1',
            'backgroundColor': '#123123',
            'foregroundColor': '#234234',
            'hidden': False,
            'selected': True,
            'defaultReminders': [
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 15}
            ],
            'notificationSettings': {
                'notifications': [
                    {'type': 'eventCreation', 'method': 'email'},
                    {'type': 'eventChange', 'method': 'email'}
                ]
            }
        }
        self.assertDictEqual(CalendarListEntrySerializer.to_json(c), expected_calendar_json)

        c = CalendarListEntry(
            summary_override='Summary override',
            calendar_id='Calendar id',
            _timezone=TEST_TIMEZONE,
        )
        expected_calendar_json = {
            'id': 'Calendar id',
            'summaryOverride': 'Summary override',
            'hidden': False,
            'selected': False,
        }
        self.assertDictEqual(CalendarListEntrySerializer.to_json(c), expected_calendar_json)

    def test_to_object(self):
        calendar_json = {
            "id": 'Calendar id',
            "summary": 'Summary',
            "description": 'Description',
            "location": 'Fiji',
            "timeZone": TEST_TIMEZONE,
            "summaryOverride": 'Summary override',
            "colorId": '1',
            "backgroundColor": '#123123',
            "foregroundColor": '#234234',
            "hidden": False,
            "selected": True,
            "accessRole": TEST_ACCESS_ROLE,
            "defaultReminders": [
                {"method": 'email', "minutes": 60},
                {"method": 'popup', "minutes": 15}
            ],
            "notificationSettings": {
                "notifications": [
                    {'type': 'eventCreation', 'method': 'email'},
                    {'type': 'eventChange', 'method': 'email'}
                ]
            },
            "primary": True,
            "deleted": False,
            "conferenceProperties": {
                "allowedConferenceSolutionTypes": TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES
            }
        }

        serializer = CalendarListEntrySerializer(calendar_json)
        c = serializer.get_object()

        self.assertEqual(c.summary_override, 'Summary override')
        self.assertEqual(c.color_id, '1')
        self.assertEqual(c.background_color, '#123123')
        self.assertEqual(c.foreground_color, '#234234')
        self.assertFalse(c.hidden)
        self.assertTrue(c.selected)
        self.assertListEqual(c.default_reminders, [EmailReminder(60), PopupReminder(15)])
        self.assertEqual(c.notification_types, TEST_NOTIFICATION_TYPES)
        self.assertEqual(c.access_role, TEST_ACCESS_ROLE)
        self.assertTrue(c.primary)
        self.assertFalse(c.deleted)

        self.assertEqual(c.summary, 'Summary')
        self.assertEqual(c.calendar_id, 'Calendar id')
        self.assertEqual(c.description, 'Description')
        self.assertEqual(c.location, 'Fiji')
        self.assertEqual(c.timezone, TEST_TIMEZONE)
        self.assertListEqual(c.allowed_conference_solution_types, TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES)

        calendar_json = """{
            "id": "Calendar id",
            "foregroundColor": "#234234",
            "defaultReminders": [
                {"method": "email", "minutes": 60},
                {"method": "popup", "minutes": 15}
            ],
            "primary": true,
            "conferenceProperties": {
                "allowedConferenceSolutionTypes": ["eventHangout", "eventNamedHangout"]
            }
        }"""

        serializer = CalendarListEntrySerializer(calendar_json)
        c = serializer.get_object()

        self.assertEqual(c.foreground_color, '#234234')
        self.assertListEqual(c.default_reminders, [EmailReminder(60), PopupReminder(15)])
        self.assertTrue(c.primary)

        self.assertEqual(c.calendar_id, 'Calendar id')
        self.assertListEqual(c.allowed_conference_solution_types, TEST_ALLOWED_CONFERENCE_SOLUTION_TYPES)
