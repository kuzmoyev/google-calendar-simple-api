from typing import List

from tzlocal import get_localzone_name

from ._resource import Resource
from .reminders import Reminder


class NotificationType:
    """
    * `EVENT_CREATION` - Notification sent when a new event is put on the calendar.
    * `EVENT_CHANGE` - Notification sent when an event is changed.
    * `EVENT_CANCELLATION` - Notification sent when an event is cancelled.
    * `EVENT_RESPONSE` - Notification sent when an attendee responds to the event invitation.
    * `AGENDA` - An agenda with the events of the day (sent out in the morning).
    """

    EVENT_CREATION = "eventCreation"
    EVENT_CHANGE = "eventChange"
    EVENT_CANCELLATION = "eventCancellation"
    EVENT_RESPONSE = "eventResponse"
    AGENDA = "agenda"


class AccessRoles:
    """
    * `FREE_BUSY_READER` - Provides read access to free/busy information.
    * `READER` - Provides read access to the calendar.
      Private events will appear to users with reader access, but event details will be hidden.
    * `WRITER` - Provides read and write access to the calendar.
      Private events will appear to users with writer access, and event details will be visible.
    * `OWNER` - Provides ownership of the calendar.
      This role has all of the permissions of the writer role with the additional ability to see and manipulate ACLs.
    """

    FREE_BUSY_READER = "freeBusyReader"
    READER = "reader"
    WRITER = "writer"
    OWNER = "owner"


class Calendar(Resource):
    def __init__(
            self,
            summary: str,
            *,
            calendar_id: str = None,
            description: str = None,
            location: str = None,
            timezone: str = get_localzone_name(),
            allowed_conference_solution_types: List[str] = None
    ):
        """
        :param summary:
                Title of the calendar.
        :param calendar_id:
                Identifier of the calendar.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
        :param description:
                Description of the calendar.
        :param location:
                Geographic location of the calendar as free-form text.
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param allowed_conference_solution_types:
                The types of conference solutions that are supported for this calendar.
                See :py:class:`~gcsa.conference.SolutionType`
        """
        self.summary = summary
        self.calendar_id = calendar_id
        self.description = description
        self.location = location
        self.timezone = timezone
        self.allowed_conference_solution_types = allowed_conference_solution_types

    @property
    def id(self):
        return self.calendar_id

    def to_calendar_list_entry(
            self,
            summary_override: str = None,
            color_id: str = None,
            background_color: str = None,
            foreground_color: str = None,
            hidden: bool = False,
            selected: bool = False,
            default_reminders: List[Reminder] = None,
            notification_types: List[str] = None,
    ) -> 'CalendarListEntry':
        """Converts :py:class:`~gcsa.calendar.Calendar` to :py:class:`~gcsa.calendar.CalendarListEntry`
        that can be added to the calendar list.

        :py:class:`~gcsa.calendar.Calendar` has to have `calendar_id` set
        to be converted to :py:class:`~gcsa.calendar.CalendarListEntry`

        :param summary_override:
                The summary that the authenticated user has set for this calendar.
        :param color_id:
                The color of the calendar. This is an ID referring to an entry in the calendar section of the colors'
                definition (See :py:meth:`~gcsa.google_calendar.GoogleCalendar.list_calendar_colors`).
                This property is superseded by the `background_color` and `foreground_color` properties
                and can be ignored when using these properties.
        :param background_color:
                The main color of the calendar in the hexadecimal format "#0088aa".
                This property supersedes the index-based color_id property.
        :param foreground_color:
                The foreground color of the calendar in the hexadecimal format "#ffffff".
                This property supersedes the index-based color_id property.
        :param hidden:
                Whether the calendar has been hidden from the list.
        :param selected:
                Whether the calendar content shows up in the calendar UI. The default is False.
        :param default_reminders:
                The default reminders that the authenticated user has for this calendar. :py:mod:`~gcsa.reminders`
        :param notification_types:
                The list of notification types set for this calendar. :py:class:`~gcsa:calendar:NotificationType`

        :return:
                :py:class:`~gcsa.calendar.CalendarListEntry` object that can be added to the calendar list.
        """
        if self.id is None:
            raise ValueError('Calendar has to have `calendar_id` set to be converted to CalendarListEntry')

        return CalendarListEntry(
            _summary=self.summary,
            calendar_id=self.calendar_id,
            _description=self.description,
            _location=self.location,
            _timezone=self.timezone,
            _allowed_conference_solution_types=self.allowed_conference_solution_types,

            summary_override=summary_override,
            color_id=color_id,
            background_color=background_color,
            foreground_color=foreground_color,
            hidden=hidden,
            selected=selected,
            default_reminders=default_reminders,
            notification_types=notification_types,
        )

    def __str__(self):
        return '{} - {}'.format(self.summary, self.description)

    def __repr__(self):
        return '<Calendar {}>'.format(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, Calendar):
            return NotImplemented
        elif self is other:
            return True
        else:
            return super().__eq__(other)


class CalendarListEntry(Calendar):
    def __init__(
            self,
            calendar_id: str,
            *,
            summary_override: str = None,
            color_id: str = None,
            background_color: str = None,
            foreground_color: str = None,
            hidden: bool = False,
            selected: bool = False,
            default_reminders: List[Reminder] = None,
            notification_types: List[str] = None,
            _summary: str = None,
            _description: str = None,
            _location: str = None,
            _timezone: str = None,
            _allowed_conference_solution_types: List[str] = None,
            _access_role: str = None,
            _primary: bool = False,
            _deleted: bool = False
    ):
        """
        :param calendar_id:
                Identifier of the calendar.
        :param summary_override:
                The summary that the authenticated user has set for this calendar.
        :param color_id:
                The color of the calendar. This is an ID referring to an entry in the calendar section of the colors'
                definition (See :py:meth:`~gcsa.google_calendar.GoogleCalendar.list_calendar_colors`).
                This property is superseded by the `background_color` and `foreground_color` properties
                and can be ignored when using these properties.
        :param background_color:
                The main color of the calendar in the hexadecimal format "#0088aa".
                This property supersedes the index-based color_id property.
        :param foreground_color:
                The foreground color of the calendar in the hexadecimal format "#ffffff".
                This property supersedes the index-based color_id property.
        :param hidden:
                Whether the calendar has been hidden from the list.
        :param selected:
                Whether the calendar content shows up in the calendar UI. The default is False.
        :param default_reminders:
                The default reminders that the authenticated user has for this calendar. :py:mod:`~gcsa.reminders`
        :param notification_types:
                The list of notification types set for this calendar. :py:class:`~gcsa:calendar:NotificationType`
        :param _summary:
                Title of the calendar. Read-only.
        :param _description:
                Description of the calendar. Read-only.
        :param _location:
                Geographic location of the calendar as free-form text. Read-only.
        :param _timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". Read-only.
        :param _allowed_conference_solution_types:
                The types of conference solutions that are supported for this calendar. Read-only.
                See :py:class:`~gcsa.conference.SolutionType`
        :param _access_role:
                The effective access role that the authenticated user has on the calendar. Read-only.
                See :py:class:`~gcsa.calendar.AccessRoles`
        :param _primary:
                Whether the calendar is the primary calendar of the authenticated user. Read-only.
        :param _deleted:
                Whether this calendar list entry has been deleted from the calendar list. Read-only.
        """
        super().__init__(
            summary=_summary,
            calendar_id=calendar_id,
            description=_description,
            location=_location,
            timezone=_timezone,
            allowed_conference_solution_types=_allowed_conference_solution_types
        )
        self.summary_override = summary_override
        self._color_id = color_id
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.hidden = hidden
        self.selected = selected
        self.default_reminders = default_reminders
        self.notification_types = notification_types
        self.access_role = _access_role
        self.primary = _primary
        self.deleted = _deleted

    @property
    def color_id(self):
        return self._color_id

    @color_id.setter
    def color_id(self, color_id):
        """Sets the color_id and resets background_color and foreground_color."""
        self._color_id = color_id
        self.background_color = None
        self.foreground_color = None

    def __str__(self):
        return '{} - ({})'.format(self.summary_override, self.summary)

    def __repr__(self):
        return '<CalendarListEntry {}>'.format(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, CalendarListEntry):
            return NotImplemented
        elif self is other:
            return True
        else:
            return super().__eq__(other)
