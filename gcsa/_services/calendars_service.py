from typing import Union

from gcsa._services.base_service import BaseService
from gcsa.calendar import Calendar, CalendarListEntry
from gcsa.serializers.calendar_serializer import CalendarSerializer


class CalendarsService(BaseService):
    """Calendars management methods of the `GoogleCalendar`"""

    def get_calendar(
            self,
            calendar_id: str = None
    ) -> Calendar:
        """Returns the calendar with the corresponding calendar_id.

        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                The corresponding :py:class:`~gcsa.calendar.Calendar` object.
        """
        calendar_id = calendar_id or self.default_calendar
        calendar_resource = self.service.calendars().get(
            calendarId=calendar_id
        ).execute()
        return CalendarSerializer.to_object(calendar_resource)

    def add_calendar(
            self,
            calendar: Calendar
    ):
        """Creates a secondary calendar.

        :param calendar:
                Calendar object.
        :return:
                Created calendar object with ID.
        """
        body = CalendarSerializer.to_json(calendar)
        calendar_json = self.service.calendars().insert(
            body=body
        ).execute()
        return CalendarSerializer.to_object(calendar_json)

    def update_calendar(
            self,
            calendar: Calendar
    ):
        """Updates metadata for a calendar.

        :param calendar:
                Calendar object with set `calendar_id`

        :return:
                Updated calendar object
        """
        calendar_id = self._get_resource_id(calendar)
        body = CalendarSerializer.to_json(calendar)
        calendar_json = self.service.calendars().update(
            calendarId=calendar_id,
            body=body
        ).execute()
        return CalendarSerializer.to_object(calendar_json)

    def delete_calendar(
            self,
            calendar: Union[Calendar, CalendarListEntry, str]
    ):
        """Deletes a secondary calendar.

        Use :py:meth:`~gcsa.google_calendar.GoogleCalendar.clear_calendar` for clearing all events on primary calendars.

        :param calendar:
                Calendar's ID or :py:class:`~gcsa.calendar.Calendar` object with set `calendar_id`.
        """
        calendar_id = self._get_resource_id(calendar)
        self.service.calendars().delete(calendarId=calendar_id).execute()

    def clear_calendar(self):
        """Clears a **primary** calendar.
        This operation deletes all events associated with the **primary** calendar of an account.

        Currently, there is no way to clear a secondary calendar.
        You can use :py:meth:`~gcsa.google_calendar.GoogleCalendar.delete_event` method with the secondary calendar's ID
        to delete events from a secondary calendar.
        """
        self.service.calendars().clear(calendarId='primary').execute()

    def clear(self):
        """Kept for back-compatibility. Use :py:meth:`~gcsa.google_calendar.GoogleCalendar.clear_calendar` instead.

        Clears a **primary** calendar.
        This operation deletes all events associated with the **primary** calendar of an account.

        Currently, there is no way to clear a secondary calendar.
        You can use :py:meth:`~gcsa.google_calendar.GoogleCalendar.delete_event` method with the secondary calendar's ID
        to delete events from a secondary calendar.
        """
        self.clear_calendar()
