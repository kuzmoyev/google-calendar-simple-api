from gcsa.reminders import Reminder, EmailReminder, PopupReminder
from .base_serializer import BaseSerializer


class ReminderSerializer(BaseSerializer):
    type_ = Reminder

    def __init__(self, reminder):
        super().__init__(reminder)

    @staticmethod
    def _to_json(reminder: Reminder):
        return {
            'method': reminder.method,
            'minutes': reminder.minutes_before_start
        }

    @staticmethod
    def _to_object(json_reminder):
        method = json_reminder['method']
        if method == 'email':
            return EmailReminder(int(json_reminder['minutes']))
        elif method == 'popup':
            return PopupReminder(int(json_reminder['minutes']))
        else:
            raise ValueError('Unexpected method "{}" for a reminder.'.format(method))
