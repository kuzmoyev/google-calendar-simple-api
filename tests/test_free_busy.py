from unittest import TestCase

from beautiful_date import Mar

from gcsa.free_busy import FreeBusy, TimeRange
from gcsa.serializers.free_busy_serializer import FreeBusySerializer


class TestFreeBusy(TestCase):
    def test_iter(self):
        free_busy = FreeBusy(
            time_min=(24 / Mar / 2023)[13:22],
            time_max=(25 / Mar / 2023)[13:22],
            groups={},
            calendars={
                'calendar1': [
                    TimeRange((24 / Mar / 2023)[14:22], (24 / Mar / 2023)[15:22]),
                    TimeRange((24 / Mar / 2023)[17:22], (24 / Mar / 2023)[18:22]),
                ]
            }
        )

        ranges = list(free_busy)
        self.assertEqual(len(ranges), 2)
        self.assertEqual(ranges[0], free_busy.calendars['calendar1'][0])
        self.assertEqual(ranges[1], free_busy.calendars['calendar1'][1])

    def test_iter_errors(self):
        free_busy = FreeBusy(
            time_min=(24 / Mar / 2023)[13:22],
            time_max=(25 / Mar / 2023)[13:22],
            groups={},
            calendars={
                'calendar1': [
                    TimeRange((24 / Mar / 2023)[14:22], (24 / Mar / 2023)[15:22]),
                    TimeRange((24 / Mar / 2023)[17:22], (24 / Mar / 2023)[18:22]),
                ],
                'calendar2': [
                    TimeRange((24 / Mar / 2023)[15:22], (24 / Mar / 2023)[16:22]),
                    TimeRange((24 / Mar / 2023)[18:22], (24 / Mar / 2023)[19:22]),
                ]
            }
        )

        with self.assertRaises(ValueError):
            iter(free_busy)

        free_busy = FreeBusy(
            time_min=(24 / Mar / 2023)[13:22],
            time_max=(25 / Mar / 2023)[13:22],
            groups={},
            calendars={
                'calendar1': [
                    TimeRange((24 / Mar / 2023)[14:22], (24 / Mar / 2023)[15:22]),
                    TimeRange((24 / Mar / 2023)[17:22], (24 / Mar / 2023)[18:22]),
                ]
            },
            calendars_errors={
                'calendar2': ['notFound']
            }
        )
        with self.assertRaises(ValueError):
            iter(free_busy)

        free_busy = FreeBusy(
            time_min=(24 / Mar / 2023)[13:22],
            time_max=(25 / Mar / 2023)[13:22],
            groups={},
            calendars={},
            calendars_errors={
                'calendar1': ['notFound']
            }
        )
        with self.assertRaises(ValueError):
            iter(free_busy)

    def test_repr_str(self):
        free_busy = FreeBusy(
            time_min=(24 / Mar / 2023)[13:22],
            time_max=(25 / Mar / 2023)[13:22],
            groups={'group1': ['calendar1', 'calendar2']},
            calendars={
                'calendar1': [
                    TimeRange((24 / Mar / 2023)[14:22], (24 / Mar / 2023)[15:22]),
                    TimeRange((24 / Mar / 2023)[17:22], (24 / Mar / 2023)[18:22]),
                ],
                'calendar2': [
                    TimeRange((24 / Mar / 2023)[15:22], (24 / Mar / 2023)[16:22]),
                    TimeRange((24 / Mar / 2023)[18:22], (24 / Mar / 2023)[19:22]),
                ]
            }
        )
        self.assertEqual(free_busy.__repr__(), "<FreeBusy 2023-03-24 13:22:00 - 2023-03-25 13:22:00>")
        self.assertEqual(free_busy.__str__(), "<FreeBusy 2023-03-24 13:22:00 - 2023-03-25 13:22:00>")


class TestFreeBusySerializer(TestCase):
    def test_to_json(self):
        free_busy = FreeBusy(
            time_min=(24 / Mar / 2023)[13:22],
            time_max=(25 / Mar / 2023)[13:22],
            groups={'group1': ['calendar1', 'calendar2']},
            calendars={
                'calendar1': [
                    TimeRange((24 / Mar / 2023)[14:22], (24 / Mar / 2023)[15:22]),
                    TimeRange((24 / Mar / 2023)[17:22], (24 / Mar / 2023)[18:22]),
                ],
                'calendar2': [
                    TimeRange((24 / Mar / 2023)[15:22], (24 / Mar / 2023)[16:22]),
                    TimeRange((24 / Mar / 2023)[18:22], (24 / Mar / 2023)[19:22]),
                ]
            },
            groups_errors={
                "non-existing-group": [
                    {
                        "domain": "global",
                        "reason": "notFound"
                    }
                ]
            },
            calendars_errors={
                "non-existing-calendar": [
                    {
                        "domain": "global",
                        "reason": "notFound"
                    }
                ]
            }
        )

        free_busy_json = FreeBusySerializer.to_json(free_busy)
        self.assertEqual(free_busy_json['timeMin'], '2023-03-24T13:22:00')
        self.assertEqual(free_busy_json['timeMax'], '2023-03-25T13:22:00')
        self.assertIn('calendar1', free_busy_json['calendars'])
        self.assertIn('calendar2', free_busy_json['calendars'])
        self.assertIn('non-existing-calendar', free_busy_json['calendars'])
        self.assertIn('group1', free_busy_json['groups'])
        self.assertIn('non-existing-group', free_busy_json['groups'])

    def test_to_object(self):
        free_busy_json = {
            'calendars': {
                'calendar1': {
                    'busy': [{'start': '2023-03-24T14:22:00', 'end': '2023-03-24T15:22:00'},
                             {'start': '2023-03-24T17:22:00', 'end': '2023-03-24T18:22:00'}],
                },
                'calendar2': {
                    'busy': [{'start': '2023-03-24T15:22:00', 'end': '2023-03-24T16:22:00'}],
                },
                'non-existing-calendar': {
                    'errors': [{'domain': 'global', 'reason': 'notFound'}]
                }
            },
            'groups': {
                'group1': {
                    'calendars': ['calendar1', 'calendar2'],
                },
                'non-existing-group': {
                    'errors': [{'domain': 'global', 'reason': 'notFound'}]
                }
            },
            'timeMin': '2023-03-24T13:22:00',
            'timeMax': '2023-03-25T13:22:00'
        }

        free_busy = FreeBusySerializer.to_object(free_busy_json)

        self.assertEqual(free_busy.time_min, (24 / Mar / 2023)[13:22])
        self.assertEqual(free_busy.time_max, (25 / Mar / 2023)[13:22])

        self.assertIn('calendar1', free_busy.calendars)
        self.assertIn('calendar2', free_busy.calendars)
        self.assertNotIn('calendar1', free_busy.calendars_errors)
        self.assertNotIn('calendar2', free_busy.calendars_errors)
        self.assertEqual(len(free_busy.calendars['calendar1']), 2)
        self.assertEqual(len(free_busy.calendars['calendar2']), 1)
        self.assertNotIn('non-existing-calendar', free_busy.calendars)
        self.assertIn('non-existing-calendar', free_busy.calendars_errors)

        self.assertIn('group1', free_busy.groups)
        self.assertNotIn('group1', free_busy.groups_errors)
        self.assertEqual(len(free_busy.groups['group1']), 2)
        self.assertIn('non-existing-group', free_busy.groups_errors)
        self.assertNotIn('non-existing-group', free_busy.groups)

        free_busy_json = """{
            "timeMin": "2023-03-24T13:22:00",
            "timeMax": "2023-03-25T13:22:00"
        }"""

        free_busy = FreeBusySerializer(free_busy_json).to_object(free_busy_json)
        self.assertEqual(free_busy.time_min, (24 / Mar / 2023)[13:22])
        self.assertEqual(free_busy.time_max, (25 / Mar / 2023)[13:22])
