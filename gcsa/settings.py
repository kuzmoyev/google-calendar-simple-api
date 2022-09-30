class Settings:
    """Represents settings that users can change from the Calendar UI, such as the user's time zone.
    They can be retrieved via :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_settings`."""

    def __init__(
            self,
            *,
            auto_add_hangouts: bool = False,
            date_field_order: str = 'MDY',
            default_event_length: int = 60,
            format24_hour_time: bool = False,
            hide_invitations: bool = False,
            hide_weekends: bool = False,
            locale: str = 'en',
            remind_on_responded_events_only: bool = False,
            show_declined_events: bool = True,
            timezone: str = 'Etc/GMT',
            use_keyboard_shortcuts: bool = True,
            week_start: int = 0
    ):
        """
            :param auto_add_hangouts:
                    Whether to automatically add Hangouts to all events.
            :param date_field_order:
                    What should the order of day (D), month (M) and year (Y) be when displaying dates.
            :param default_event_length:
                    The default length of events (in minutes) that were created without an explicit duration.
            :param format24_hour_time:
                    Whether to show the time in 24-hour format.
            :param hide_invitations:
                    Whether to hide events to which the user is invited but hasn't acted on (for example by responding).
            :param hide_weekends:
                    Whether the weekends should be hidden when displaying a week.
            :param locale:
                    User's locale.
            :param remind_on_responded_events_only:
                    Whether event reminders should be sent only for events with the user's response status "Yes" and
                    "Maybe".
            :param show_declined_events:
                    Whether events to which the user responded "No" should be shown on the user's calendar.
            :param timezone:
                    The ID of the user's timezone.
            :param use_keyboard_shortcuts:
                    Whether the keyboard shortcuts are enabled.
            :param week_start:
                    Whether the week should start on Sunday (0), Monday (1) or Saturday (6).
        """
        self.auto_add_hangouts = auto_add_hangouts
        self.date_field_order = date_field_order
        self.default_event_length = default_event_length
        self.format24_hour_time = format24_hour_time
        self.hide_invitations = hide_invitations
        self.hide_weekends = hide_weekends
        self.locale = locale
        self.remind_on_responded_events_only = remind_on_responded_events_only
        self.show_declined_events = show_declined_events
        self.timezone = timezone
        self.use_keyboard_shortcuts = use_keyboard_shortcuts
        self.week_start = week_start

    def __str__(self):
        return f'User settings:\n' \
               f'auto_add_hangouts={self.auto_add_hangouts}\n' \
               f'date_field_order={self.date_field_order}\n' \
               f'default_event_length={self.default_event_length}\n' \
               f'format24_hour_time={self.format24_hour_time}\n' \
               f'hide_invitations={self.hide_invitations}\n' \
               f'hide_weekends={self.hide_weekends}\n' \
               f'locale={self.locale}\n' \
               f'remind_on_responded_events_only={self.remind_on_responded_events_only}\n' \
               f'show_declined_events={self.show_declined_events}\n' \
               f'timezone={self.timezone}\n' \
               f'use_keyboard_shortcuts={self.use_keyboard_shortcuts}\n' \
               f'week_start={self.week_start}'

    def __repr__(self):
        return self.__str__()
