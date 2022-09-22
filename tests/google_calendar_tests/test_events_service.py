from beautiful_date import D, days, years, hours

from gcsa.event import Event
from gcsa.util.date_time_util import ensure_localisation
from tests.mock_services.util import TestCaseWithMockedService


class TestEventsService(TestCaseWithMockedService):

    def test_get_events_default(self):
        events = list(self.gc.get_events())
        self.assertEqual(len(events), 10)
        self.assertFalse(any(e.is_recurring_instance for e in events))

        events = list(self.gc)
        self.assertEqual(len(events), 10)
        self.assertFalse(any(e.is_recurring_instance for e in events))

    def test_get_events_time_limits(self):
        time_min = ensure_localisation(D.today()[:] + 5 * days)
        events = list(self.gc.get_events(time_min=time_min))
        self.assertEqual(len(events), 6)
        self.assertTrue(all(e.start >= time_min for e in events))

        time_min = ensure_localisation(D.today()[:] + 5 * days)
        events = list(self.gc[time_min])
        self.assertEqual(len(events), 6)
        self.assertTrue(all(e.start >= time_min for e in events))

        time_max = ensure_localisation(D.today()[:] + 1 * years + 7 * days)
        events = list(self.gc.get_events(time_max=time_max))
        self.assertEqual(len(events), 11)
        self.assertTrue(all(e.end < time_max for e in events))

        time_max = ensure_localisation(D.today()[:] + 7 * days)
        events = list(self.gc.get_events(time_max=time_max))
        self.assertEqual(len(events), 7)
        self.assertTrue(all(e.end < time_max for e in events))

        events = list(self.gc.get_events(time_min=time_min, time_max=time_max))
        self.assertEqual(len(events), 2)
        self.assertTrue(all(time_min <= e.start and e.end < time_max for e in events))

        events = list(self.gc[time_min:time_max])
        self.assertEqual(len(events), 2)
        self.assertTrue(all(time_min <= e.start and e.end < time_max for e in events))

        time_min = D.today() + 5 * days
        time_max = D.today() + 7 * days
        events = list(self.gc.get_events(time_min=time_min, time_max=time_max))
        self.assertEqual(len(events), 3)

        time_min = ensure_localisation(time_min[0:0])
        time_max = ensure_localisation(time_max[23:59:59])
        self.assertTrue(all(time_min <= e.start and e.end < time_max for e in events))

        with self.assertRaises(NotImplementedError):
            _ = self.gc[5]
        with self.assertRaises(ValueError):
            _ = self.gc[5:10]

    def test_get_events_single_events(self):
        events = list(self.gc.get_events(single_events=True))
        self.assertEqual(len(events), 19)
        self.assertTrue(all(e.is_recurring_instance for e in events if e.summary == 'Recurring event'))

        events = list(self.gc.get_events(single_events=False))
        self.assertEqual(len(events), 10)
        self.assertTrue(all(not e.is_recurring_instance for e in events if e.summary == 'Recurring event'))

        with self.assertRaises(ValueError):
            # can only be used with single events
            list(self.gc.get_events(order_by='startTime'))

    def test_get_events_order_by(self):
        events = list(self.gc.get_events(order_by='updated'))
        self.assertEqual(len(events), 10)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.updated).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.updated).id)

        events = list(self.gc[::'updated'])
        self.assertEqual(len(events), 10)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.updated).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.updated).id)

        events = list(self.gc[::'startTime'])
        self.assertEqual(len(events), 19)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.start).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.start).id)

        events = list(self.gc.get_events(order_by='startTime', single_events=True))
        self.assertEqual(len(events), 19)
        self.assertEqual(events[0].id, min(events, key=lambda e: e.start).id)
        self.assertEqual(events[-1].id, max(events, key=lambda e: e.start).id)

    def test_get_events_query(self):
        events = list(self.gc.get_events(query='test4', time_max=D.today()[:] + 2 * years))
        self.assertEqual(len(events), 2)  # test4 and test42

        events = list(self.gc.get_events(query='Jo', time_max=D.today()[:] + 2 * years))
        self.assertEqual(len(events), 2)  # with John and Josh

        events = list(self.gc.get_events(query='Josh', time_max=D.today()[:] + 2 * years))
        self.assertEqual(len(events), 1)

        events = list(self.gc.get_events(query='Frank', time_max=D.today()[:] + 2 * years))
        self.assertEqual(len(events), 1)

    def test_get_recurring_instances(self):
        events = list(self.gc.get_instances(recurring_event='event_id_1'))
        self.assertEqual(len(events), 9)
        self.assertTrue(all(e.id.startswith('event_id_1') for e in events))

        recurring_event = Event(
            'recurring event',
            D.today()[:],
            event_id='event_id_2'
        )
        events = list(self.gc.get_instances(recurring_event=recurring_event))
        self.assertEqual(len(events), 4)
        self.assertTrue(all(e.id.startswith('event_id_2') for e in events))

    def test_get_event(self):
        start = D.today()[:]
        end = start + 2 * hours
        event = Event(
            'test_event',
            start=start,
            end=end
        )
        new_event = self.gc.add_event(event)

        received_new_event = self.gc.get_event(new_event.id)
        self.assertEqual(received_new_event, new_event)

    def test_add_event(self):
        start = D.today()[:]
        end = start + 2 * hours
        event = Event(
            'test_event',
            start=start,
            end=end
        )
        new_event = self.gc.add_event(event)

        self.assertIsNotNone(new_event.id)

        received_new_event = self.gc.get_event(new_event.id)
        self.assertEqual(received_new_event, new_event)

    def test_add_quick_event(self):
        start = ensure_localisation(D.today()[:])
        summary = 'Breakfast'
        event_string = f'{summary} at {start.isoformat()}'

        new_event = self.gc.add_quick_event(event_string)

        self.assertIsNotNone(new_event.id)
        self.assertEqual(new_event.summary, summary)
        self.assertEqual(new_event.start, start)

        received_new_event = self.gc.get_event(new_event.id)
        self.assertEqual(received_new_event, new_event)

    def test_update_event(self):
        start = ensure_localisation(D.today()[:])
        summary = 'test_event'
        event = Event(
            summary,
            start=start
        )
        new_event = self.gc.add_event(event)
        self.assertEqual(new_event.summary, summary)

        new_summary = 'test_event_updated'
        new_start = start + 1 * days

        new_event.summary = new_summary
        new_event.start = new_start

        updated_event = self.gc.update_event(new_event)
        self.assertEqual(updated_event, new_event)

        received_updated_event = self.gc.get_event(new_event.id)
        self.assertEqual(received_updated_event, new_event)

    def test_import_event(self):
        start = D.today()[:]
        end = start + 2 * hours
        event = Event(
            'test_event',
            start=start,
            end=end,
            event_id='test_event'
        )
        new_event = self.gc.import_event(event)
        received_new_event = self.gc.get_event(new_event.id)
        self.assertEqual(received_new_event, new_event)

    def test_move_event(self):
        start = D.today()[:]
        end = start + 2 * hours
        event = Event(
            'test_event',
            start=start,
            end=end,
            event_id='test_event_id'
        )
        new_event = self.gc.add_event(event)
        received_new_event = self.gc.move_event(new_event, destination_calendar_id='test_dest_calendar')
        self.assertEqual(received_new_event, new_event)

    def test_delete_event(self):
        start = D.today()[:]
        end = start + 2 * hours
        event = Event(
            'test_event',
            start=start,
            end=end
        )
        with self.assertRaises(ValueError):
            # no event_id
            self.gc.delete_event(event)

        new_event = self.gc.add_event(event)
        self.gc.delete_event(new_event)
        self.gc.delete_event('test_event_id')

        with self.assertRaises(TypeError):
            # should be event or event id as a string
            self.gc.delete_event(start)
