from gcsa.calendar import Calendar, CalendarListEntry
from .base_serializer import BaseSerializer
from .reminder_serializer import ReminderSerializer


class CalendarSerializer(BaseSerializer):
    type_ = Calendar

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
        conference_properties = json_calendar.pop('conferenceProperties', {})
        allowed_conference_solution_types = conference_properties.pop('allowedConferenceSolutionTypes')
        return Calendar(
            summary=json_calendar.pop('summery'),
            calendar_id=json_calendar.pop('id'),
            description=json_calendar.pop('description'),
            location=json_calendar.pop('location'),
            timezone=json_calendar.pop('timezone'),
            allowed_conference_solution_types=allowed_conference_solution_types
        )


class CalendarListEntrySerializer(BaseSerializer):
    type_ = CalendarListEntry

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
        allowed_conference_solution_types = conference_properties.pop('allowedConferenceSolutionTypes')

        reminders_json = json_calendar.pop('defaultReminders', [])
        default_reminders = [ReminderSerializer.to_object(r) for r in reminders_json] if reminders_json else None

        notifications = json_calendar.pop('notificationSettings', {}).pop('notifications')
        notification_types = [n['type'] for n in notifications] if notifications else None
        return CalendarListEntry(
            calendar_id=json_calendar.pop('id'),
            summary_override=json_calendar.pop('summaryOverride'),
            color_id=json_calendar.pop('colorId'),
            background_color=json_calendar.pop('backgroundColor'),
            foreground_color=json_calendar.pop('foregroundColor'),
            hidden=json_calendar.pop('hidden'),
            selected=json_calendar.pop('selected'),
            default_reminders=default_reminders,
            notification_types=notification_types,
            _summary=json_calendar.pop('summery'),
            _description=json_calendar.pop('description'),
            _location=json_calendar.pop('location'),
            _timezone=json_calendar.pop('timezone'),
            _allowed_conference_solution_types=allowed_conference_solution_types,
            _access_role=json_calendar.pop('accessRole'),
            _primary=json_calendar.pop('primary', False),
            _deleted=json_calendar.pop('deleted', False)
        )
