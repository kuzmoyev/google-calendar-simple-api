from datetime import time, datetime, date
from unittest import TestCase

from beautiful_date import Apr

from gcsa.reminders import Reminder, EmailReminder, PopupReminder
from gcsa.serializers.reminder_serializer import ReminderSerializer


class TestReminder(TestCase):
    def test_email_reminder(self):
        reminder = EmailReminder()
        self.assertEqual(reminder.method, 'email')
        self.assertEqual(reminder.minutes_before_start, 60)

        reminder = EmailReminder(34)
        self.assertEqual(reminder.method, 'email')
        self.assertEqual(reminder.minutes_before_start, 34)

        reminder = EmailReminder(days_before=1, at=time(0, 0))
        self.assertEqual(reminder.method, 'email')
        self.assertEqual(reminder.minutes_before_start, None)
        self.assertEqual(reminder.days_before, 1)
        self.assertEqual(reminder.at, time(0, 0))

    def test_popup_reminder(self):
        reminder = PopupReminder()
        self.assertEqual(reminder.method, 'popup')
        self.assertEqual(reminder.minutes_before_start, 30)

        reminder = PopupReminder(51)
        self.assertEqual(reminder.method, 'popup')
        self.assertEqual(reminder.minutes_before_start, 51)

        reminder = PopupReminder(days_before=1, at=time(0, 0))
        self.assertEqual(reminder.method, 'popup')
        self.assertEqual(reminder.minutes_before_start, None)
        self.assertEqual(reminder.days_before, 1)
        self.assertEqual(reminder.at, time(0, 0))

    def test_repr_str(self):
        reminder = EmailReminder(34)
        self.assertEqual(reminder.__repr__(), "<EmailReminder - minutes_before_start:34>")
        self.assertEqual(reminder.__str__(), "EmailReminder - minutes_before_start:34")

        reminder = PopupReminder(days_before=1, at=time(0, 0))
        self.assertEqual(reminder.__repr__(), "<PopupReminder - 1 days before at 00:00:00>")
        self.assertEqual(reminder.__str__(), "PopupReminder - 1 days before at 00:00:00")

    def test_absolute_reminders_conversion(self):
        absolute_reminder = EmailReminder(days_before=1, at=time(12, 0))
        reminder = absolute_reminder.convert_to_relative(datetime(2024, 4, 16, 10, 15))
        self.assertEqual(reminder.method, 'email')
        self.assertEqual(reminder.minutes_before_start, (12 + 10) * 60 + 15)

        absolute_reminder = PopupReminder(days_before=2, at=time(11, 30))
        reminder = absolute_reminder.convert_to_relative(date(2024, 4, 16))
        self.assertEqual(reminder.method, 'popup')
        self.assertEqual(reminder.minutes_before_start, 24 * 60 + 12 * 60 + 30)

        absolute_reminder = PopupReminder(days_before=5, at=time(10, 25))
        reminder = absolute_reminder.convert_to_relative(16 / Apr / 2024)
        self.assertEqual(reminder.method, 'popup')
        self.assertEqual(reminder.minutes_before_start, 4 * 24 * 60 + 13 * 60 + 35)

    def test_reminder_checks(self):
        # No time provided
        with self.assertRaises(ValueError):
            Reminder(method='email')

        # Both relative and absolute times provided
        with self.assertRaises(ValueError):
            Reminder(method='email', minutes_before_start=22, days_before=1)
        with self.assertRaises(ValueError):
            Reminder(method='email', minutes_before_start=22, at=time(0, 0))

        # Only one of days_before and at provided
        with self.assertRaises(ValueError):
            Reminder(method='email', days_before=1)
        with self.assertRaises(ValueError):
            Reminder(method='email', at=time(0, 0))
        with self.assertRaises(ValueError):
            PopupReminder(days_before=1)
        with self.assertRaises(ValueError):
            EmailReminder(at=time(0, 0))


class TestReminderSerializer(TestCase):
    def test_to_json(self):
        reminder_json = {
            'method': 'email',
            'minutes': 55
        }
        reminder = EmailReminder(55)

        self.assertDictEqual(ReminderSerializer.to_json(reminder), reminder_json)

        reminder_json = {
            'method': 'popup',
            'minutes': 13
        }
        reminder = PopupReminder(13)

        self.assertDictEqual(ReminderSerializer.to_json(reminder), reminder_json)

        serializer = ReminderSerializer(reminder)
        self.assertDictEqual(serializer.get_json(), reminder_json)

    def test_to_object(self):
        reminder_json = {
            'method': 'email',
            'minutes': 55
        }

        reminder = ReminderSerializer.to_object(reminder_json)

        self.assertIsInstance(reminder, EmailReminder)
        self.assertEqual(reminder.minutes_before_start, 55)

        reminder_json = {
            'method': 'popup',
            'minutes': 33
        }

        reminder = ReminderSerializer.to_object(reminder_json)

        self.assertIsInstance(reminder, PopupReminder)
        self.assertEqual(reminder.minutes_before_start, 33)

        reminder_json_str = """{
            "method": "popup",
            "minutes": 22
        }"""

        reminder = ReminderSerializer.to_object(reminder_json_str)

        self.assertIsInstance(reminder, PopupReminder)
        self.assertEqual(reminder.minutes_before_start, 22)

        with self.assertRaises(ValueError):
            reminder_json = {
                'method': 'telegram',
                'minutes': 33
            }

            ReminderSerializer.to_object(reminder_json)
