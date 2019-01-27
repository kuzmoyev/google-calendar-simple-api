from tzlocal import get_localzone
from datetime import datetime, date, timedelta

from .attachment import Attachment
from .reminder import PopupReminder, EmailReminder
from util.date_time_util import insure_localisation


class Visibility:
    """ Possible values of the event visibility.

    DEFAULT - Uses the default visibility for events on the calendar. This is the default value.
    PUBLIC - The event is public and event details are visible to all readers of the calendar.
    PRIVATE - The event is private and only event attendees may view event details.
    """

    DEFAULT = "default"
    PUBLIC = "public"
    PRIVATE = "private"


class Event:
    def __init__(self,
                 summary,
                 start,
                 end=None,
                 timezone=str(get_localzone()),
                 event_id=None,
                 description=None,
                 location=None,
                 recurrence=None,
                 color=None,
                 visibility=Visibility.DEFAULT,
                 gadget=None,
                 attachments=None,
                 reminders=None,
                 default_reminders=False,
                 minutes_before_popup_reminder=None,
                 minutes_before_email_reminder=None,
                 **other):
        """
        :param summary:
                title of the event.
        :param start:
                starting date/datetime.
        :param end:
                ending date/datetime. If 'end' is not specified, event is considered as a 1-day or 1-hour event
                if 'start' is date or datetime respectively.
        :param timezone:
                timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers configured local timezone(if any) is used.
        :param event_id:
                opaque identifier of the event. By default is generated by the server. You can specify id as a
                5-1024 long string of characters used in base32hex ([a-vA-V0-9]). The ID must be unique per
                calendar.
        :param description:
                description of the event.
        :param location:
                geographic location of the event as free-form text.
        :param recurrence:
                RRULE/RDATE/EXRULE/EXDATE string or list of such strings. TODO link to code.
        :param color:
                color id referring to an entry from colors endpoint (list_event_colors)
        :param visibility:
                visibility of the event. Default is default visibility for events on the calendar.
        :param gadget:
                a gadget that extends the event. TODO link to code.
        :param attachments:
                attachment or list of attachments. TODO link to code.
        :param reminders:
                reminder or list of reminder objects. TODO link to code.
        :param default_reminders:
                whether the default reminders of the calendar apply to the event.
        :param minutes_before_popup_reminder:
                minutes before popup reminder or None if reminder is not needed.
        :param minutes_before_email_reminder:
                minutes before email reminder or None if reminder is not needed.
        :param other:
                Other fields that should be included in request json. Will be included as they are.
        """

        def assure_list(obj):
            return obj if isinstance(obj, list) else obj or []

        self.timezone = timezone
        self.start = start
        if end:
            self.end = end
        elif isinstance(start, datetime):
            self.end = start + timedelta(hours=1)
        elif isinstance(start, date):
            self.end = start + timedelta(days=1)

        if isinstance(self.start, datetime) and isinstance(self.end, datetime):
            self.start = insure_localisation(self.start, timezone)
            self.end = insure_localisation(self.end, timezone)
        elif isinstance(self.start, datetime) or isinstance(self.end, datetime):
            raise TypeError('Start and end must either both be date or both be datetime.')

        reminders = assure_list(reminders)

        if len(reminders) > 5:
            raise ValueError('The maximum number of override reminders is 5.')

        if default_reminders and reminders:
            raise ValueError('Cannot specify both default reminders and overrides at the same time.')

        self.event_id = event_id and event_id.lower()
        self.summary = summary
        self.description = description
        self.location = location
        self.recurrence = assure_list(recurrence)
        self.color_id = color
        self.visibility = visibility
        self.gadget = gadget
        self.attachments = assure_list(attachments)
        self.reminders = reminders
        self.default_reminders = default_reminders
        self.other = other

        if minutes_before_popup_reminder:
            self.add_popup_reminder(minutes_before_popup_reminder)
        if minutes_before_email_reminder:
            self.add_email_reminder(minutes_before_email_reminder)

    def get_id(self):
        return self.event_id

    def add_attachment(self, file_url, title, mime_type):
        self.attachments.append(Attachment(title=title, file_url=file_url, mime_type=mime_type))

    def add_email_reminder(self, minutes_before_start=60):
        self.add_reminder(EmailReminder(minutes_before_start))

    def add_popup_reminder(self, minutes_before_start=30):
        self.add_reminder(PopupReminder(minutes_before_start))

    def add_reminder(self, reminder):
        if len(self.reminders) > 4:
            raise ValueError('The maximum number of override reminders is 5.')
        self.reminders.append(reminder)

    def __str__(self):
        return '{} - {}'.format(self.start, self.summary)
