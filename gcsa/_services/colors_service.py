from gcsa._services.base_service import BaseService


class ColorsService(BaseService):
    """Colors management methods of the `GoogleCalendar`"""

    def list_event_colors(self) -> dict:
        """A global palette of event colors, mapping from the color ID to its definition.
        An :py:class:`~gcsa.event.Event` may refer to one of these color IDs in its color_id field."""
        return self.service.colors().get().execute()['event']

    def list_calendar_colors(self) -> dict:
        """A global palette of calendar colors, mapping from the color ID to its definition.
        :py:class:`~gcsa.calendar.CalendarListEntry` resource refers to one of these color IDs in its color_id field."""
        return self.service.colors().get().execute()['calendar']
