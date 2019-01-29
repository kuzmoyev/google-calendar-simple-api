from unittest import TestCase

from gcsa.reminders import EmailReminder, PopupReminder
from gcsa.serializers.reminder_serializer import ReminderSerializer


class TestReminder(TestCase):
    def test_email_reminder(self):
        reminder = EmailReminder(34)
        self.assertEqual(reminder.method, 'email')
        self.assertEqual(reminder.minutes_before_start, 34)

    def test_popup_reminder(self):
        reminder = PopupReminder(51)
        self.assertEqual(reminder.method, 'popup')
        self.assertEqual(reminder.minutes_before_start, 51)


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

        with self.assertRaises(ValueError):
            reminder_json = {
                'method': 'telegram',
                'minutes': 33
            }

            ReminderSerializer.to_object(reminder_json)
