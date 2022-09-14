from gcsa.calendar import Calendar, CalendarListEntry
from .base_serializer import BaseSerializer
from .reminder_serializer import ReminderSerializer


class CalendarSerializer(BaseSerializer):
    type_ = Calendar

    def __init__(self, calendar):
        super().__init__(calendar)

    @staticmethod
    def _to_json(calendar: Calendar):
        data = {
            "id": calendar.calendar_id,
            "summary": calendar.summary,
            "description": calendar.description,
            "location": calendar.location,
            "timeZone": calendar.timezone,
        }
        if calendar.allowed_conference_solution_types:
            data["conferenceProperties"] = {
                "allowedConferenceSolutionTypes": calendar.allowed_conference_solution_types
            }

        data = CalendarSerializer._remove_empty_values(data)

        return data

    @staticmethod
    def _to_object(json_calendar):
        conference_properties = json_calendar.get('conferenceProperties', {})
        allowed_conference_solution_types = conference_properties.get('allowedConferenceSolutionTypes')
        return Calendar(
            summary=json_calendar.get('summary'),
            calendar_id=json_calendar.get('id'),
            description=json_calendar.get('description'),
            location=json_calendar.get('location'),
            timezone=json_calendar.get('timeZone'),
            allowed_conference_solution_types=allowed_conference_solution_types
        )


class CalendarListEntrySerializer(BaseSerializer):
    type_ = CalendarListEntry

    def __init__(self, calendar_list_entry):
        super().__init__(calendar_list_entry)

    @staticmethod
    def _to_json(calendar: CalendarListEntry):
        data = {
            "id": calendar.calendar_id,
            "summaryOverride": calendar.summary_override,
            "colorId": calendar.color_id,
            "backgroundColor": calendar.background_color,
            "foregroundColor": calendar.foreground_color,
            "hidden": calendar.hidden,
            "selected": calendar.selected,

        }
        if calendar.default_reminders:
            data["defaultReminders"] = [ReminderSerializer.to_json(r) for r in calendar.default_reminders]

        if calendar.notification_types:
            data["notificationSettings"] = {
                "notifications": [
                    {
                        "type": notification_type,
                        "method": "email"
                    }
                    for notification_type in calendar.notification_types
                ]
            }

        data = CalendarListEntrySerializer._remove_empty_values(data)

        return data

    @staticmethod
    def _to_object(json_calendar):
        conference_properties = json_calendar.pop('conferenceProperties', {})
        allowed_conference_solution_types = conference_properties.pop('allowedConferenceSolutionTypes', None)

        reminders_json = json_calendar.pop('defaultReminders', [])
        default_reminders = [ReminderSerializer.to_object(r) for r in reminders_json] if reminders_json else None

        notifications = json_calendar.pop('notificationSettings', {}).pop('notifications', None)
        notification_types = [n['type'] for n in notifications] if notifications else None

        return CalendarListEntry(
            calendar_id=json_calendar.pop('id'),
            summary_override=json_calendar.pop('summaryOverride', None),
            color_id=json_calendar.pop('colorId', None),
            background_color=json_calendar.pop('backgroundColor', None),
            foreground_color=json_calendar.pop('foregroundColor', None),
            hidden=json_calendar.pop('hidden', False),
            selected=json_calendar.pop('selected', False),
            default_reminders=default_reminders,
            notification_types=notification_types,
            _summary=json_calendar.pop('summary', None),
            _description=json_calendar.pop('description', None),
            _location=json_calendar.pop('location', None),
            _timezone=json_calendar.pop('timeZone', None),
            _allowed_conference_solution_types=allowed_conference_solution_types,
            _access_role=json_calendar.pop('accessRole', None),
            _primary=json_calendar.pop('primary', False),
            _deleted=json_calendar.pop('deleted', False)
        )
