from beautiful_date import D, days, years

from gcsa.event import Event
from gcsa.util.date_time_util import insure_localisation
from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestEventsService(TestCaseWithMockedService):

    def test_get_events_default(self):
        events = list(self.gc.get_events())
        self.assertEqual(len(events), 10)
        self.assertFalse(any(e.is_recurring_instance for e in events))

        events = list(self.gc)
        self.assertEqual(len(events), 10)
        self.assertFalse(any(e.is_recurring_instance for e in events))

    def test_get_events_time_limits(self):
        time_min = insure_localisation(D.today()[:] + 5 * days)
        events = list(self.gc.get_events(time_min=time_min))
        self.assertEqual(len(events), 6)
        self.assertTrue(all(e.start >= time_min for e in events))

        time_min = insure_localisation(D.today()[:] + 5 * days)
        events = list(self.gc[time_min])
        self.assertEqual(len(events), 6)
        self.assertTrue(all(e.start >= time_min for e in events))

        time_max = insure_localisation(D.today()[:] + 1 * years + 7 * days)
        events = list(self.gc.get_events(time_max=time_max))
        self.assertEqual(len(events), 11)
        self.assertTrue(all(e.end < time_max for e in events))

        time_max = insure_localisation(D.today()[:] + 7 * days)
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

        time_min = insure_localisation(time_min[0:0])
        time_max = insure_localisation(time_max[23:59:59])
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
