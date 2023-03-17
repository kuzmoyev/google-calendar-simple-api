from .util import executable

import dateutil.parser
from beautiful_date import D, days, years

from gcsa.attendee import Attendee
from gcsa.event import Event
from gcsa.serializers.event_serializer import EventSerializer
from gcsa.util.date_time_util import ensure_localisation


class MockEventsRequests:
    """Emulates GoogleCalendar.service.events()"""

    EVENTS_PER_PAGE = 3

    def __init__(self):
        self.test_events = [
            Event(
                'test{}'.format(i),
                start=ensure_localisation(D.today()[i:0] + i * days),
                event_id=f'event_id_{str(i)}',
                _updated=ensure_localisation(D.today()[i:0] + (i + 1) * days),
                attendees=[
                    Attendee(email='{}@gmail.com'.format(attendee_name.lower()), display_name=attendee_name)
                ] if attendee_name else None
            )
            for i, attendee_name in zip(range(1, 10), ['John', 'Josh'] + [''] * 8)
        ]

    @property
    def test_events_by_id(self):
        return {e.id: e for e in self.test_events}

    @executable
    def instances(self, eventId, **_):
        """Emulates GoogleCalendar.service.events().instances().execute()"""

        if eventId == 'event_id_1':
            recurring_instances = [
                Event(
                    'Recurring event 1',
                    start=D.today()[:] + 1 * days,
                    event_id='event_id_1_' + (D.today()[:] + (i + 1) * days).isoformat() + 'Z',
                    _updated=D.today()[:] + 5 * days,
                    _recurring_event_id='event_id_1',

                ) for i in range(1, 10)
            ]
        elif eventId == 'event_id_2':
            recurring_instances = [
                Event(
                    'Recurring event 2',
                    start=D.today()[:] + 2 * days,
                    event_id='event_id_2_' + (D.today()[:] + (i + 2) * days).isoformat() + 'Z',
                    _updated=D.today()[:] + 5 * days,
                    _recurring_event_id='event_id_2',

                ) for i in range(1, 5)
            ]
        else:
            # shouldn't get here in tests
            raise ValueError(f'Event with id {eventId} does not exist')

        return {
            'items': recurring_instances,
            'nextPageToken': None
        }

    @executable
    def list(self, timeMin, timeMax, orderBy, singleEvents, pageToken, q, **_):
        """Emulates GoogleCalendar.service.events().list().execute()"""

        time_min = dateutil.parser.parse(timeMin)
        time_max = dateutil.parser.parse(timeMax)
        page = pageToken or 0  # page number in this case

        test_events = self.test_events.copy()

        recurring_event = Event('Recurring event',
                                start=ensure_localisation(D.today()[:] + 2 * days),
                                event_id='recurring_id',
                                _updated=ensure_localisation(D.today()[:] + 3 * days))
        recurring_instances = [
            Event(
                recurring_event.summary,
                start=recurring_event.start + i * days,
                event_id=recurring_event.id + '_' + (recurring_event.start + i * days).isoformat() + 'Z',
                _updated=recurring_event.updated,
                _recurring_event_id=recurring_event.id,

            ) for i in range(10)
        ]

        if singleEvents:
            test_events.extend(recurring_instances)
        else:
            test_events.append(recurring_event)

        event_in_a_year = Event(
            'test42',
            start=ensure_localisation(D.today()[:] + 1 * years + 2 * days),
            event_id='42',
            _updated=ensure_localisation(D.today()[:] + 1 * years + 3 * days),
            attendees=[
                Attendee(email='frank@gmail.com', display_name='Frank')
            ]
        )
        test_events.append(event_in_a_year)

        def _filter(e):
            return (
                    (time_min <= e.start and e.end < time_max) and
                    (
                            not q or
                            q in e.summary or
                            (e.description and q in e.description) or
                            (e.attendees and any((a.display_name and q in a.display_name) for a in e.attendees))
                    )
            )

        def _sort_key(e):
            if orderBy is None:
                return e.id
            if orderBy == 'startTime':
                return e.start
            if orderBy == 'updated':
                return e.updated

        filtered_events = list(filter(_filter, test_events))
        ordered_events = sorted(filtered_events, key=_sort_key)
        serialized_events = list(map(EventSerializer.to_json, ordered_events))

        current_page_events = ordered_events[page * self.EVENTS_PER_PAGE:(page + 1) * self.EVENTS_PER_PAGE]
        next_page = page + 1 if (page + 1) * self.EVENTS_PER_PAGE < len(serialized_events) else None
        return {
            'items': current_page_events,
            'nextPageToken': next_page
        }

    @executable
    def get(self, eventId, **_):
        """Emulates GoogleCalendar.service.events().get().execute()"""
        try:
            return EventSerializer.to_json(self.test_events_by_id[eventId])
        except KeyError:
            # shouldn't get here in tests
            raise ValueError(f'Event with id {eventId} does not exist')

    @executable
    def insert(self, body, **_):
        """Emulates GoogleCalendar.service.events().insert().execute()"""
        event = EventSerializer.to_object(body)

        if event.id is None:
            event.event_id = f'event_id_{len(self.test_events) + 1}'
        else:
            assert event.id not in self.test_events_by_id

        self.test_events.append(event)
        return EventSerializer.to_json(event)

    @executable
    def quickAdd(self, text, **_):
        """Emulates GoogleCalendar.service.events().quickAdd().execute()"""
        summary, start = text.split(' at ')
        event = Event(
            summary,
            start=dateutil.parser.parse(start)
        )

        event.event_id = f'event_id_{len(self.test_events) + 1}'
        self.test_events.append(event)
        return EventSerializer.to_json(event)

    @executable
    def update(self, eventId, body, **_):
        """Emulates GoogleCalendar.service.events().update().execute()"""

        updated_event = EventSerializer.to_object(body)
        for i in range(len(self.test_events)):
            if eventId == self.test_events[i].id:
                self.test_events[i] = updated_event
                return EventSerializer.to_json(updated_event)

        # shouldn't get here in tests
        raise ValueError(f'Event with id {eventId} does not exist')

    @executable
    def import_(self, body, **_):
        """Emulates GoogleCalendar.service.events().import_().execute()"""
        return self.insert(body).execute()

    @executable
    def move(self, eventId, destination, **_):
        """Emulates GoogleCalendar.service.events().move().execute()"""
        return self.get(eventId=eventId).execute()

    @executable
    def delete(self, eventId, **_):
        """Emulates GoogleCalendar.service.events().delete().execute()"""
        self.test_events = [e for e in self.test_events if e.id != eventId]
