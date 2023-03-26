from datetime import date, datetime
from typing import Union, Iterator, Iterable, Callable

from beautiful_date import BeautifulDate
from dateutil.relativedelta import relativedelta
from tzlocal import get_localzone_name

from gcsa._services.base_service import BaseService
from gcsa.event import Event
from gcsa.serializers.event_serializer import EventSerializer
from gcsa.util.date_time_util import to_localized_iso


class SendUpdatesMode:
    """Possible values of the mode for sending updates or invitations to attendees.

    * ALL - Send updates to all participants. This is the default value.
    * EXTERNAL_ONLY - Send updates only to attendees not using google calendar.
    * NONE - Do not send updates.
    """

    ALL = "all"
    EXTERNAL_ONLY = "externalOnly"
    NONE = "none"


class EventsService(BaseService):
    """Event management methods of the `GoogleCalendar`"""

    def _list_events(
            self,
            request_method: Callable,
            time_min: Union[date, datetime, BeautifulDate],
            time_max: Union[date, datetime, BeautifulDate],
            timezone: str,
            calendar_id: str,
            **kwargs
    ) -> Iterable[Event]:
        """Lists paginated events received from request_method."""

        time_min = time_min or datetime.now()
        time_max = time_max or time_min + relativedelta(years=1)

        time_min = to_localized_iso(time_min, timezone)
        time_max = to_localized_iso(time_max, timezone)

        yield from self._list_paginated(
            request_method,
            serializer_cls=EventSerializer,
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            **kwargs
        )

    def get_events(
            self,
            time_min: Union[date, datetime, BeautifulDate] = None,
            time_max: Union[date, datetime, BeautifulDate] = None,
            order_by: str = None,
            timezone: str = get_localzone_name(),
            single_events: bool = False,
            query: str = None,
            calendar_id: str = None,
            **kwargs
    ) -> Iterable[Event]:
        """Lists events.

        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param order_by:
                Order of the events. Possible values: "startTime", "updated". Default is unspecified stable order.
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param single_events:
                Whether to expand recurring events into instances and only return single one-off events and
                instances of recurring events, but not the underlying recurring events themselves.
        :param query:
                Free text search terms to find events that match these terms in any field, except for
                extended properties.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/list#optional-parameters

        :return:
                Iterable of `Event` objects
        """
        calendar_id = calendar_id or self.default_calendar
        if not single_events and order_by == 'startTime':
            raise ValueError(
                '"startTime" ordering is only available when querying single events, i.e. single_events=True'
            )
        yield from self._list_events(
            self.service.events().list,
            time_min=time_min,
            time_max=time_max,
            timezone=timezone,
            calendar_id=calendar_id,
            **{
                'singleEvents': single_events,
                'orderBy': order_by,
                'q': query,
                **kwargs
            }
        )

    def get_instances(
            self,
            recurring_event: Union[Event, str],
            time_min: Union[date, datetime, BeautifulDate] = None,
            time_max: Union[date, datetime, BeautifulDate] = None,
            timezone: str = get_localzone_name(),
            calendar_id: str = None,
            **kwargs
    ) -> Iterable[Event]:
        """Lists instances of recurring event

        :param recurring_event:
                Recurring event or instance of recurring event (`Event` object) or id of the recurring event
        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/instances#optional-parameters

        :return:
                Iterable of event objects
        """
        calendar_id = calendar_id or self.default_calendar
        try:
            event_id = self._get_resource_id(recurring_event)
        except ValueError:
            raise ValueError("Recurring event has to have id to retrieve its instances.")

        yield from self._list_events(
            self.service.events().instances,
            time_min=time_min,
            time_max=time_max,
            timezone=timezone,
            calendar_id=calendar_id,
            **{
                'eventId': event_id,
                **kwargs
            }
        )

    def __iter__(self) -> Iterator[Event]:
        return iter(self.get_events())

    def __getitem__(self, r):
        if isinstance(r, slice):
            time_min, time_max, order_by = r.start or None, r.stop or None, r.step or None
        elif isinstance(r, (date, datetime)):
            time_min, time_max, order_by = r, None, None
        else:
            raise NotImplementedError

        if (
                (time_min and not isinstance(time_min, (date, datetime)))
                or (time_max and not isinstance(time_max, (date, datetime)))
                or (order_by and (not isinstance(order_by, str) or order_by not in self._LIST_ORDERS))
        ):
            raise ValueError('Calendar indexing is in the following format:  time_min[:time_max[:order_by]],'
                             ' where time_min and time_max are date/datetime objects'
                             ' and order_by is None or one of "startTime" or "updated" strings.')

        return self.get_events(time_min, time_max, order_by=order_by, single_events=(order_by == "startTime"))

    def get_event(
            self,
            event_id: str,
            calendar_id: str = None,
            **kwargs
    ) -> Event:
        """Returns the event with the corresponding event_id.

        :param event_id:
                The unique event ID.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/get#optional-parameters
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                The corresponding event object.
        """
        calendar_id = calendar_id or self.default_calendar
        event_resource = self.service.events().get(
            calendarId=calendar_id,
            eventId=event_id,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_resource)

    def add_event(
            self,
            event: Event,
            send_updates: str = SendUpdatesMode.NONE,
            calendar_id: str = None,
            **kwargs
    ) -> Event:
        """Creates event in the calendar

        :param event:
                Event object.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/insert#optional-parameters

        :return:
                Created event object with id.
        """
        calendar_id = calendar_id or self.default_calendar
        body = EventSerializer.to_json(event)
        event_json = self.service.events().insert(
            calendarId=calendar_id,
            body=body,
            conferenceDataVersion=1,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def add_quick_event(
            self,
            event_string: str,
            send_updates: str = SendUpdatesMode.NONE,
            calendar_id: str = None,
            **kwargs
    ) -> Event:
        """Creates event in the calendar by string description.

        Example:
            Appointment at Somewhere on June 3rd 10am-10:25am

        :param event_string:
                String that describes an event
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/quickAdd#optional-parameters

        :return:
                Created event object with id.
        """
        calendar_id = calendar_id or self.default_calendar
        event_json = self.service.events().quickAdd(
            calendarId=calendar_id,
            text=event_string,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def update_event(
            self,
            event: Event,
            send_updates: str = SendUpdatesMode.NONE,
            calendar_id: str = None,
            **kwargs
    ) -> Event:
        """Updates existing event in the calendar

        :param event:
                Event object with set `event_id`.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/update#optional-parameters

        :return:
                Updated event object.
        """
        calendar_id = calendar_id or self.default_calendar
        event_id = self._get_resource_id(event)
        body = EventSerializer.to_json(event)
        event_json = self.service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=body,
            conferenceDataVersion=1,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def import_event(
            self,
            event: Event,
            calendar_id: str = None,
            **kwargs
    ) -> Event:
        """Imports an event in the calendar

        This operation is used to add a private copy of an existing event to a calendar.

        :param event:
                Event object.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/import#optional-parameters

        :return:
                Created event object with id.
        """
        calendar_id = calendar_id or self.default_calendar
        body = EventSerializer.to_json(event)
        event_json = self.service.events().import_(
            calendarId=calendar_id,
            body=body,
            conferenceDataVersion=1,
            **kwargs
        ).execute()
        return EventSerializer.to_object(event_json)

    def move_event(
            self,
            event: Event,
            destination_calendar_id: str,
            send_updates: str = SendUpdatesMode.NONE,
            source_calendar_id: str = None,
            **kwargs
    ) -> Event:
        """Moves existing event from calendar to another calendar

        :param event:
                Event object with set event_id.
        :param destination_calendar_id:
                ID of the destination calendar.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param source_calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/move#optional-parameters

        :return:
                Moved event object.
        """
        source_calendar_id = source_calendar_id or self.default_calendar
        event_id = self._get_resource_id(event)
        moved_event_json = self.service.events().move(
            calendarId=source_calendar_id,
            eventId=event_id,
            destination=destination_calendar_id,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
        return EventSerializer.to_object(moved_event_json)

    def delete_event(
            self,
            event: Union[Event, str],
            send_updates: str = SendUpdatesMode.NONE,
            calendar_id: str = None,
            **kwargs
    ):
        """Deletes an event.

        :param event:
                Event's ID or `Event` object with set `event_id`.
        :param send_updates:
                Whether and how to send updates to attendees. See :py:class:`~gcsa.google_calendar.SendUpdatesMode`
                Default is "NONE".
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/delete#optional-parameters
        """
        calendar_id = calendar_id or self.default_calendar
        event_id = self._get_resource_id(event)

        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
            sendUpdates=send_updates,
            **kwargs
        ).execute()
