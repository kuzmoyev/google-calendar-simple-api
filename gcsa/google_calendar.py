from datetime import date, datetime
import pickle
import os.path
from typing import List, Union, Callable, Iterable, Iterator, Type

from beautiful_date import BeautifulDate
from dateutil.relativedelta import relativedelta
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tzlocal import get_localzone

from .calendar import Calendar, CalendarListEntry
from .event import Event
from .serializers.calendar_serializer import CalendarSerializer, CalendarListEntrySerializer
from .serializers.event_serializer import EventSerializer
from .util.date_time_util import insure_localisation


class SendUpdatesMode:
    """Possible values of the mode for sending updates or invitations to attendees.

    * ALL - Send updates to all participants. This is the default value.
    * EXTERNAL_ONLY - Send updates only to attendees not using google calendar.
    * NONE - Do not send updates.
    """

    ALL = "all"
    EXTERNAL_ONLY = "externalOnly"
    NONE = "none"


class GoogleCalendar:
    _READ_WRITE_SCOPES = 'https://www.googleapis.com/auth/calendar'
    _LIST_ORDERS = ("startTime", "updated")

    def __init__(
            self,
            calendar: str = 'primary',
            *,
            credentials: Credentials = None,
            credentials_path: str = None,
            token_path: str = None,
            save_token: bool = True,
            read_only: bool = False,
            authentication_flow_host: str = 'localhost',
            authentication_flow_port: int = 8080
    ):
        """Represents Google Calendar of the user.

        Specify ``credentials`` to use in requests or ``credentials_path`` and ``token_path`` to get credentials from.

        :param calendar:
                Users email address or name/id of the calendar. Default: primary calendar of the user

                If user's email or "primary" is specified, then primary calendar of the user is used.
                You don't need to specify this parameter in this case as it is a default behaviour.

                To use a different calendar you need to specify its id.
                Go to calendar's `settings and sharing` -> `Integrate calendar` -> `Calendar ID`.
        :param credentials:
                Credentials with token and refresh token.
                If specified, ``credentials_path``, ``token_path``, and ``save_token`` are ignored.
                If not specified, credentials are retrieved from "token.pickle" file (specified in ``token_path`` or
                default path) or with authentication flow using secret from "credentials.json" (specified in
                ``credentials_path`` or default path)
        :param credentials_path:
                Path to "credentials.json" file. Default: ~/.credentials
        :param token_path:
                Existing path to load the token from, or path to save the token after initial authentication flow.
                Default: "token.pickle" in the same directory as the credentials_path
        :param save_token:
                Whether to pickle token after authentication flow for future uses
        :param read_only:
                If require read only access. Default: False
        :param authentication_flow_host:
                Host to receive response during authentication flow
        :param authentication_flow_port:
                Port to receive response during authentication flow
        """

        if credentials:
            self.credentials = self._ensure_refreshed(credentials)
        else:
            credentials_path = credentials_path or GoogleCalendar._get_default_credentials_path()
            credentials_dir, credentials_file = os.path.split(credentials_path)
            token_path = token_path or os.path.join(credentials_dir, 'token.pickle')
            scopes = [self._READ_WRITE_SCOPES + ('.readonly' if read_only else '')]

            self.credentials = self._get_credentials(
                token_path,
                credentials_dir,
                credentials_file,
                scopes,
                save_token,
                authentication_flow_host,
                authentication_flow_port
            )

        self.default_calendar = calendar
        self.service = discovery.build('calendar', 'v3', credentials=self.credentials)

    @staticmethod
    def _ensure_refreshed(
            credentials: Credentials
    ) -> Credentials:
        if not credentials.valid and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        return credentials

    @staticmethod
    def _get_credentials(
            token_path: str,
            credentials_dir: str,
            credentials_file: str,
            scopes: List[str],
            save_token: bool,
            host: str,
            port: int
    ) -> Credentials:
        credentials = None

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token_file:
                credentials = pickle.load(token_file)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials_path = os.path.join(credentials_dir, credentials_file)
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                credentials = flow.run_local_server(host=host, port=port)

            if save_token:
                with open(token_path, 'wb') as token_file:
                    pickle.dump(credentials, token_file)

        return credentials

    @staticmethod
    def _get_default_credentials_path() -> str:
        """Checks if ".credentials" folder in home directory exists. If not, creates it.
        :return: expanded path to .credentials folder
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'credentials.json')
        return credential_path

    @staticmethod
    def _list_paginated(
            request_method: Callable,
            serializer_cls: Type,
            **kwargs
    ):
        page_token = None
        while True:
            response_json = request_method(
                **kwargs,
                pageToken=page_token
            ).execute()
            for item_json in response_json['items']:
                yield serializer_cls(item_json).get_object()
            page_token = response_json.get('nextPageToken')
            if not page_token:
                break

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

        if not isinstance(time_min, datetime):
            time_min = datetime.combine(time_min, datetime.min.time())

        if not isinstance(time_max, datetime):
            time_max = datetime.combine(time_max, datetime.max.time())

        time_min = insure_localisation(time_min, timezone).isoformat()
        time_max = insure_localisation(time_max, timezone).isoformat()

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
            timezone: str = str(get_localzone()),
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/list#optional-parameters

        :return:
                Iterable of `Event` objects
        """
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
            recurring_event,
            time_min=None,
            time_max=None,
            timezone=str(get_localzone()),
            calendar_id: str = None,
            **kwargs
    ) -> Iterable[Event]:
        """Lists instances of recurring event

        :param recurring_event:
                Recurring event (Event object) or id of a recurring event
        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/instances#optional-parameters

        :return:
                Iterable of event objects
        """
        yield from self._list_events(
            self.service.events().instances,
            time_min=time_min,
            time_max=time_max,
            timezone=timezone,
            calendar_id=calendar_id,
            **{
                'eventId': recurring_event if isinstance(recurring_event, str) else recurring_event.id,
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/update#optional-parameters

        :return:
                Updated event object.
        """
        calendar_id = calendar_id or self.default_calendar
        body = EventSerializer.to_json(event)
        event_json = self.service.events().update(
            calendarId=calendar_id,
            eventId=event.id,
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/move#optional-parameters

        :return:
                Moved event object.
        """
        source_calendar_id = source_calendar_id or self.default_calendar
        moved_event_json = self.service.events().move(
            calendarId=source_calendar_id,
            eventId=event.id,
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
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/delete#optional-parameters
        """
        calendar_id = calendar_id or self.default_calendar
        if isinstance(event, Event):
            if event.id is None:
                raise ValueError("Event has to have event_id to be deleted.")
            event_id = event.id
        elif isinstance(event, str):
            event_id = event
        else:
            raise TypeError('"event" object must me Event or str, not {!r}'.format(event.__class__.__name__))

        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
            sendUpdates=send_updates,
            **kwargs
        ).execute()

    def get_calendar(
            self,
            calendar_id: str = None
    ) -> Calendar:
        """Returns the calendar with the corresponding calendar_id.

        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                The corresponding `Calendar` object.
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
        body = CalendarSerializer.to_json(calendar)
        calendar_json = self.service.calendars().update(
            calendarId=calendar.id,
            body=body
        ).execute()
        return CalendarSerializer.to_object(calendar_json)

    def delete_calendar(
            self,
            calendar: Calendar
    ):
        """Deletes a secondary calendar.

        Use :py:meth:`gcsa.google_calendar.GoogleCalendar.clear_calendar` for clearing all events on primary calendars.

        :param calendar:
                Calendar's ID or `Calendar` object with set `calendar_id`.
        """
        if isinstance(calendar, (Calendar, CalendarListEntry)):
            if calendar.id is None:
                raise ValueError("Calendar has to have calendar_id to be deleted.")
            calendar_id = calendar.id
        elif isinstance(calendar, str):
            calendar_id = calendar
        else:
            raise TypeError('"calendar" object must me Calendar or str, not {!r}'.format(calendar.__class__.__name__))

        self.service.calendars().delete(calendarId=calendar_id).execute()

    def clear_calendar(self):
        """Clears a **primary** calendar.
        This operation deletes all events associated with the **primary** calendar of an account.

        Currently, there is no way to clear a secondary calendar.
        You can use :py:meth:`gcsa.google_calendar.GoogleCalendar.delete_event` method with the secondary calendar's ID
        to delete events from a secondary calendar.
        """
        self.service.calendars().clear(calendarId='primary').execute()

    def clear(self):
        """Kept for back-compatibility. Use :py:meth:`gcsa.google_calendar.GoogleCalendar.clear_calendar` instead.

        Clears a **primary** calendar.
        This operation deletes all events associated with the **primary** calendar of an account.

        Currently, there is no way to clear a secondary calendar.
        You can use :py:meth:`gcsa.google_calendar.GoogleCalendar.delete_event` method with the secondary calendar's ID
        to delete events from a secondary calendar.
        """
        self.clear_calendar()

    def get_calendars_list(
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
                Iterable of `CalendarListEntry` objects.
        """
        yield from self._list_paginated(
            self.service.calendarList().list,
            serializer_cls=CalendarListEntrySerializer,
            minAccessRole=min_access_role,
            showDeleted=show_deleted,
            showHidden=show_hidden,
        )

    def get_calendars_list_entry(
            self,
            calendar_id: str = None
    ) -> CalendarListEntry:
        """Returns a calendar with the corresponding calendar_id from the user's calendar list.

        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`
                To retrieve calendar IDs call the :py:meth:`gcsa.google_calendar.GoogleCalendar.get_calendars_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                The corresponding `CalendarListEntry` object.
        """
        calendar_id = calendar_id or self.default_calendar
        calendar_resource = self.service.calendarList().get(calendarId=calendar_id).execute()
        return CalendarListEntrySerializer.to_object(calendar_resource)

    def add_calendars_list_entry(
            self,
            calendar: CalendarListEntry,
            color_rgb_format: bool = None
    ) -> CalendarListEntry:
        """Adds an existing calendar into the user's calendar list.

        :param calendar:
                CalendarListEntry object.
        :param color_rgb_format:
                Whether to use the `foreground_color` and `background_color` fields to write the calendar colors (RGB).
                If this feature is used, the index-based color_id field will be set to the best matching option
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

    def update_calendars_list_entry(
            self,
            calendar: CalendarListEntry,
            color_rgb_format: bool = None
    ) -> CalendarListEntry:
        """Updates an existing calendar on the user's calendar list.

        :param calendar:
                Calendar object with set `calendar_id`
        :param color_rgb_format:
                Whether to use the `foreground_color` and `background_color` fields to write the calendar colors (RGB).
                If this feature is used, the index-based color_id field will be set to the best matching option
                automatically. The default is True if `foreground_color` or `background_color` is set, False otherwise.

        :return:
                Updated calendar list entry object
        """
        if color_rgb_format is None:
            color_rgb_format = calendar.foreground_color is not None or calendar.background_color is not None

        body = CalendarListEntrySerializer.to_json(calendar)
        calendar_json = self.service.calendarList().update(
            calendarId=calendar.id,
            body=body,
            colorRgbFormat=color_rgb_format
        ).execute()
        return CalendarListEntrySerializer.to_object(calendar_json)

    def delete_calendars_list_entry(
            self,
            calendar: Calendar
    ):
        """Removes a calendar from the user's calendar list.

        :param calendar:
                Calendar's ID or `Calendar` object with set `calendar_id`.
        """
        if isinstance(calendar, (Calendar, CalendarListEntry)):
            if calendar.id is None:
                raise ValueError("Calendar has to have calendar_id to be deleted.")
            calendar_id = calendar.id
        elif isinstance(calendar, str):
            calendar_id = calendar
        else:
            raise TypeError(
                '"calendar" object must me Calendar or str, not {!r}'.format(calendar.__class__.__name__)
            )
        self.service.calendarList().delete(calendarId=calendar_id).execute()

    def list_event_colors(self) -> dict:
        """A global palette of event colors, mapping from the color ID to its definition.
        An :py:class:`~gcsa.event.Event` may refer to one of these color IDs in its color_id field."""
        return self.service.colors().get().execute()['event']

    def list_calendar_colors(self) -> dict:
        """A global palette of calendar colors, mapping from the color ID to its definition.
        :py:class:`~gcsa.calendar.CalendarListEntry` resource refers to one of these color IDs in its color_id field."""
        return self.service.colors().get().execute()['calendar']
