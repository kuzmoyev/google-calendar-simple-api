from gcsa.calendar import CalendarListEntry
from gcsa.serializers.calendar_serializer import CalendarListEntrySerializer
from .util import executable


class MockCalendarListRequests:
    """Emulates GoogleCalendar.service.calendarList()"""
    CALENDAR_LIST_ENTRIES_PER_PAGE = 3

    def __init__(self):
        self.test_calendars = [
            CalendarListEntry(
                summary_override=f'Summery override {i}',
                _summary=f'Secondary {i}',
                calendar_id=str(i)
            )
            for i in range(7)
        ]
        self.test_calendars.append(
            CalendarListEntry(
                summary_override='Primary',
                _summary='Primary',
                calendar_id='primary'
            )
        )

    @property
    def test_calendars_by_id(self):
        return {c.id: c for c in self.test_calendars}

    @executable
    def list(self, pageToken, **_):
        page = pageToken or 0  # page number in this case
        page_calendars = self.test_calendars[
                         page * self.CALENDAR_LIST_ENTRIES_PER_PAGE:(page + 1) * self.CALENDAR_LIST_ENTRIES_PER_PAGE
                         ]
        next_page = page + 1 if (page + 1) * self.CALENDAR_LIST_ENTRIES_PER_PAGE < len(self.test_calendars) else None

        return {
            'items': [
                CalendarListEntrySerializer.to_json(c)
                for c in page_calendars
            ],
            'nextPageToken': next_page
        }

    @executable
    def get(self, calendarId):
        """Emulates GoogleCalendar.service.calendarList().get().execute()"""
        try:
            return CalendarListEntrySerializer.to_json(self.test_calendars_by_id[calendarId])
        except KeyError:
            # shouldn't get here in tests
            raise ValueError(f'Calendar with id {calendarId} does not exist')

    @executable
    def insert(self, body, colorRgbFormat):
        """Emulates GoogleCalendar.service.calendarList().insert().execute()"""
        calendar = CalendarListEntrySerializer.to_object(body)
        self.test_calendars.append(calendar)
        return CalendarListEntrySerializer.to_json(calendar)

    @executable
    def update(self, calendarId, body, colorRgbFormat):
        """Emulates GoogleCalendar.service.calendars().insert().execute()"""
        calendar = CalendarListEntrySerializer.to_object(body)
        for i in range(len(self.test_calendars)):
            if calendarId == self.test_calendars[i].id:
                self.test_calendars[i] = calendar
                return CalendarListEntrySerializer.to_json(calendar)

        # shouldn't get here in tests
        raise ValueError(f'Calendar with id {calendarId} does not exist')

    @executable
    def delete(self, calendarId):
        """Emulates GoogleCalendar.service.calendars().delete().execute()"""
        self.test_calendars = [c for c in self.test_calendars if c.id != calendarId]
