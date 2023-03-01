from gcsa.calendar import Calendar, AccessRoles
from gcsa.serializers.calendar_serializer import CalendarSerializer
from .util import executable


class MockCalendarsRequests:
    """Emulates GoogleCalendar.service.calendars()"""

    def __init__(self):
        self.test_calendars = [
            Calendar(
                summary=f'Secondary {i}',
                calendar_id=str(i),
                description=f'Description {i}',
                location=f'Location {i}',
                timezone=f'Timezone {i}',
                allowed_conference_solution_types=[
                    AccessRoles.FREE_BUSY_READER,
                    AccessRoles.READER
                ]
            )
            for i in range(7)
        ]
        self.test_calendars.append(
            Calendar(
                summary='Primary',
                calendar_id='primary',
                description='Description',
                location='Location',
                timezone='Timezone',
                allowed_conference_solution_types=[
                    AccessRoles.FREE_BUSY_READER,
                    AccessRoles.READER,
                    AccessRoles.WRITER,
                    AccessRoles.OWNER,
                ]
            )
        )

    @property
    def test_calendars_by_id(self):
        return {c.id: c for c in self.test_calendars}

    @executable
    def get(self, calendarId):
        """Emulates GoogleCalendar.service.calendars().get().execute()"""
        try:
            return CalendarSerializer.to_json(self.test_calendars_by_id[calendarId])
        except KeyError:
            # shouldn't get here in tests
            raise ValueError(f'Calendar with id {calendarId} does not exist')

    @executable
    def insert(self, body):
        """Emulates GoogleCalendar.service.calendars().insert().execute()"""
        calendar = CalendarSerializer.to_object(body)
        calendar.calendar_id = str(len(self.test_calendars))
        self.test_calendars.append(calendar)
        return CalendarSerializer.to_json(calendar)

    @executable
    def update(self, calendarId, body):
        """Emulates GoogleCalendar.service.calendars().update().execute()"""
        calendar = CalendarSerializer.to_object(body)
        for i in range(len(self.test_calendars)):
            if calendarId == self.test_calendars[i].id:
                self.test_calendars[i] = calendar
                return CalendarSerializer.to_json(calendar)

        # shouldn't get here in tests
        raise ValueError(f'Calendar with id {calendarId} does not exist')

    @executable
    def delete(self, calendarId):
        """Emulates GoogleCalendar.service.calendars().delete().execute()"""
        self.test_calendars = [c for c in self.test_calendars if c.id != calendarId]

    @executable
    def clear(self, calendarId):
        """Emulates GoogleCalendar.service.calendars().clear().execute()"""
        pass
