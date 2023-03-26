from typing import Iterable, Union

from gcsa._services.base_service import BaseService
from gcsa.calendar import CalendarListEntry, Calendar
from gcsa.serializers.calendar_serializer import CalendarListEntrySerializer


class CalendarListService(BaseService):
    """Calendar list management methods of the `GoogleCalendar`"""

    def get_calendar_list(
            self,
            min_access_role: str = None,
            show_deleted: bool = False,
            show_hidden: bool = False
    ) -> Iterable[CalendarListEntry]:
        """Returns the calendars on the user's calendar list.

        :param min_access_role:
                The minimum access role for the user in the returned entries. See :py:class:`~gcsa.calendar.AccessRoles`
                The default is no restriction.
        :param show_deleted:
                Whether to include deleted calendar list entries in the result. The default is False.
        :param show_hidden:
                Whether to show hidden entries. The default is False.

        :return:
                Iterable of :py:class:`~gcsa.calendar.CalendarListEntry` objects.
        """
        yield from self._list_paginated(
            self.service.calendarList().list,
            serializer_cls=CalendarListEntrySerializer,
            minAccessRole=min_access_role,
            showDeleted=show_deleted,
            showHidden=show_hidden,
        )

    def get_calendar_list_entry(
            self,
            calendar_id: str = None
    ) -> CalendarListEntry:
        """Returns a calendar with the corresponding calendar_id from the user's calendar list.

        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                The corresponding :py:class:`~gcsa.calendar.CalendarListEntry` object.
        """
        calendar_id = calendar_id or self.default_calendar
        calendar_resource = self.service.calendarList().get(calendarId=calendar_id).execute()
        return CalendarListEntrySerializer.to_object(calendar_resource)

    def add_calendar_list_entry(
            self,
            calendar: CalendarListEntry,
            color_rgb_format: bool = None
    ) -> CalendarListEntry:
        """Adds an existing calendar into the user's calendar list.

        :param calendar:
                :py:class:`~gcsa.calendar.CalendarListEntry` object.
        :param color_rgb_format:
                Whether to use the `foreground_color` and `background_color` fields to write the calendar colors (RGB).
                If this feature is used, the index-based `color_id` field will be set to the best matching option
                automatically. The default is True if `foreground_color` or `background_color` is set, False otherwise.

        :return:
                Created `CalendarListEntry` object with id.
        """
        if color_rgb_format is None:
            color_rgb_format = (calendar.foreground_color is not None) or (calendar.background_color is not None)

        body = CalendarListEntrySerializer.to_json(calendar)
        calendar_json = self.service.calendarList().insert(
            body=body,
            colorRgbFormat=color_rgb_format
        ).execute()
        return CalendarListEntrySerializer.to_object(calendar_json)

    def update_calendar_list_entry(
            self,
            calendar: CalendarListEntry,
            color_rgb_format: bool = None
    ) -> CalendarListEntry:
        """Updates an existing calendar on the user's calendar list.

        :param calendar:
                :py:class:`~gcsa.calendar.Calendar` object with set `calendar_id`
        :param color_rgb_format:
                Whether to use the `foreground_color` and `background_color` fields to write the calendar colors (RGB).
                If this feature is used, the index-based color_id field will be set to the best matching option
                automatically. The default is True if `foreground_color` or `background_color` is set, False otherwise.

        :return:
                Updated calendar list entry object
        """
        calendar_id = self._get_resource_id(calendar)
        if color_rgb_format is None:
            color_rgb_format = calendar.foreground_color is not None or calendar.background_color is not None

        body = CalendarListEntrySerializer.to_json(calendar)
        calendar_json = self.service.calendarList().update(
            calendarId=calendar_id,
            body=body,
            colorRgbFormat=color_rgb_format
        ).execute()
        return CalendarListEntrySerializer.to_object(calendar_json)

    def delete_calendar_list_entry(
            self,
            calendar: Union[Calendar, CalendarListEntry, str]
    ):
        """Removes a calendar from the user's calendar list.

        :param calendar:
                Calendar's ID or :py:class:`~gcsa.calendar.Calendar`/:py:class:`~gcsa.calendar.CalendarListEntry` object
                with the set `calendar_id`.
        """
        calendar_id = self._get_resource_id(calendar)
        self.service.calendarList().delete(calendarId=calendar_id).execute()
