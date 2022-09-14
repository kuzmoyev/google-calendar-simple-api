from .util import executable

import dateutil
from beautiful_date import D, days, years, hours

from gcsa.attendee import Attendee
from gcsa.event import Event
from gcsa.serializers.event_serializer import EventSerializer
from gcsa.util.date_time_util import insure_localisation


class MockEventsRequests:
    """Emulates GoogleCalendar.service.events()"""

    EVENTS_PER_PAGE = 3

    @executable
    def instances(self, **kwargs):
        event_id = kwargs.pop('eventId')

        if event_id == 'event_id_1':
            recurring_instances = [
                Event(
                    'Recurring event 1',
                    start=D.today()[:] + 1 * days,
                    event_id='event_id_1_' + (D.today()[:] + (i + 1) * days).isoformat() + 'Z',
                    _updated=D.today()[:] + 5 * days,
                    _recurring_event_id='event_id_1',

                ) for i in range(1, 10)
            ]
        elif event_id == 'event_id_2':
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
            raise ValueError

        return {
            'items': recurring_instances,
            'nextPageToken': None
        }

    @executable
    def list(self, **kwargs):
        """Emulates GoogleCalendar.service.events().list().execute()"""

        time_min = dateutil.parser.parse(kwargs['timeMin'])
        time_max = dateutil.parser.parse(kwargs['timeMax'])
        order_by = kwargs['orderBy']
        single_events = kwargs['singleEvents']
        page_token = kwargs['pageToken'] or 0  # page number in this case
        q = kwargs['q']

        test_events = [
            Event(
                'test{}'.format(i),
                start=insure_localisation(D.today()[:] + i * days + i * hours),
                event_id='1',
                _updated=insure_localisation(D.today()[:] + (i + 1) * days + i * hours),
                attendees=[
                    Attendee(email='{}@gmail.com'.format(attendee_name.lower()), display_name=attendee_name)
                ] if attendee_name else None
            )
            for i, attendee_name in zip(range(1, 10), ['John', 'Josh'] + [''] * 8)
        ]

        recurring_event = Event('Recurring event',
                                start=insure_localisation(D.today()[:] + 2 * days),
                                event_id='recurring_id',
                                _updated=insure_localisation(D.today()[:] + 3 * days))
        recurring_instances = [
            Event(
                recurring_event.summary,
                start=recurring_event.start + i * days,
                event_id=recurring_event.id + '_' + (recurring_event.start + i * days).isoformat() + 'Z',
                _updated=recurring_event.updated,
                _recurring_event_id=recurring_event.id,

            ) for i in range(10)
        ]

        if single_events:
            test_events.extend(recurring_instances)
        else:
            test_events.append(recurring_event)

        event_in_a_year = Event(
            'test42',
            start=insure_localisation(D.today()[:] + 1 * years + 2 * days),
            event_id='42',
            _updated=insure_localisation(D.today()[:] + 1 * years + 3 * days),
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
            if order_by is None:
                return e.id
            if order_by == 'startTime':
                return e.start
            if order_by == 'updated':
                return e.updated

        filtered_events = list(filter(_filter, test_events))
        ordered_events = sorted(filtered_events, key=_sort_key)
        serialized_events = list(map(self._serialize_event, ordered_events))

        current_page_events = ordered_events[page_token * self.EVENTS_PER_PAGE:(page_token + 1) * self.EVENTS_PER_PAGE]
        return {
            'items': current_page_events,
            'nextPageToken': page_token + 1 if (page_token + 1) * 3 < len(serialized_events) else None
        }

    @staticmethod
    def _serialize_event(e):
        event_json = EventSerializer.to_json(e)
        event_json['updated'] = e.updated.isoformat() + 'Z'
        return event_json
