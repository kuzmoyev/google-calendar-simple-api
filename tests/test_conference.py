from unittest import TestCase

from gcsa.conference import EntryPoint, ConferenceSolution, ConferenceSolutionCreateRequest, SolutionType, \
    _BaseConferenceSolution
from gcsa.serializers.conference_serializer import EntryPointSerializer, ConferenceSolutionSerializer, \
    ConferenceSolutionCreateRequestSerializer


class TestBaseConferenceSolution(TestCase):

    def test_init(self):
        conference_solution = _BaseConferenceSolution(
            conference_id='hello',
            signature='signature',
            notes='important notes'
        )
        self.assertEqual(conference_solution.conference_id, 'hello')
        self.assertEqual(conference_solution.signature, 'signature')
        self.assertEqual(conference_solution.notes, 'important notes')

    def test_notes_length(self):
        with self.assertRaises(ValueError):
            _BaseConferenceSolution(notes='*' * 2049)

    def test_eq(self):
        conference_solution = _BaseConferenceSolution(
            conference_id='hello',
            signature='signature',
            notes='important notes'
        )
        self.assertFalse(conference_solution == 5)
        self.assertTrue(conference_solution == conference_solution)


class TestEntryPoint(TestCase):
    def test_init(self):
        entry_point = EntryPoint(
            EntryPoint.VIDEO,
            uri='https://video-conf.com/123123',
            label='label',
            pin='rU9xzGHz',
            access_code='sUhk4QPn',
            meeting_code='sUhk4QPn',
            passcode='YKa7m4D6',
            password='JW7t7f35'
        )

        self.assertEqual(entry_point.entry_point_type, EntryPoint.VIDEO)
        self.assertEqual(entry_point.uri, 'https://video-conf.com/123123')
        self.assertEqual(entry_point.label, 'label')
        self.assertEqual(entry_point.pin, 'rU9xzGHz')
        self.assertEqual(entry_point.access_code, 'sUhk4QPn')
        self.assertEqual(entry_point.meeting_code, 'sUhk4QPn')
        self.assertEqual(entry_point.passcode, 'YKa7m4D6')
        self.assertEqual(entry_point.password, 'JW7t7f35')

    def test_checks(self):
        with self.assertRaises(ValueError):
            EntryPoint('Offline')
        with self.assertRaises(ValueError):
            EntryPoint(EntryPoint.PHONE, label='a' * 513)
        with self.assertRaises(ValueError):
            EntryPoint(EntryPoint.PHONE, pin='a' * 129)
        with self.assertRaises(ValueError):
            EntryPoint(EntryPoint.PHONE, access_code='a' * 129)
        with self.assertRaises(ValueError):
            EntryPoint(EntryPoint.PHONE, meeting_code='a' * 129)
        with self.assertRaises(ValueError):
            EntryPoint(EntryPoint.PHONE, passcode='a' * 129)
        with self.assertRaises(ValueError):
            EntryPoint(EntryPoint.PHONE, password='a' * 129)

    def test_eq(self):
        entry_point = EntryPoint(
            EntryPoint.VIDEO,
            uri='https://video-conf.com/123123',
            label='label',
            pin='rU9xzGHz',
            access_code='sUhk4QPn',
            meeting_code='sUhk4QPn',
            passcode='YKa7m4D6',
            password='JW7t7f35'
        )
        self.assertFalse(entry_point == 5)
        self.assertTrue(entry_point == entry_point)

    def test_repr_str(self):
        entry_point = EntryPoint(
            EntryPoint.VIDEO,
            uri='https://video-conf.com/123123',
            label='label',
            pin='rU9xzGHz',
            access_code='sUhk4QPn',
            meeting_code='sUhk4QPn',
            passcode='YKa7m4D6',
            password='JW7t7f35'
        )
        self.assertEqual(entry_point.__repr__(), "<EntryPoint video - 'https://video-conf.com/123123'>")
        self.assertEqual(entry_point.__str__(), "video - 'https://video-conf.com/123123'")


class TestEntryPointSerializer(TestCase):
    def test_to_json(self):
        entry_point = EntryPoint(
            EntryPoint.SIP,
            uri='sip:123123',
            label='label',
            pin='rU9xzGHz',
            access_code='sUhk4QPn',
            meeting_code='sUhk4QPn',
            passcode='YKa7m4D6',
            password='JW7t7f35'
        )
        expected = {
            'entryPointType': 'sip',
            'uri': 'sip:123123',
            'label': 'label',
            'pin': 'rU9xzGHz',
            'accessCode': 'sUhk4QPn',
            'meetingCode': 'sUhk4QPn',
            'passcode': 'YKa7m4D6',
            'password': 'JW7t7f35'
        }

        serializer = EntryPointSerializer(entry_point)
        self.assertDictEqual(serializer.get_json(), expected)

        entry_point = EntryPoint(
            EntryPoint.MORE,
            uri='https://less.com',
            pin='rU9xzGHz',
            meeting_code='sUhk4QPn',
            password='JW7t7f35'
        )

        expected = {
            'entryPointType': 'more',
            'uri': 'https://less.com',
            'pin': 'rU9xzGHz',
            'meetingCode': 'sUhk4QPn',
            'password': 'JW7t7f35'
        }

        self.assertDictEqual(EntryPointSerializer.to_json(entry_point), expected)

    def test_to_object(self):
        entry_point_json = {
            'entryPointType': 'sip',
            'uri': 'sip:123123',
            'label': 'label',
            'pin': 'rU9xzGHz',
            'accessCode': 'sUhk4QPn',
            'meetingCode': 'sUhk4QPn',
            'passcode': 'YKa7m4D6',
            'password': 'JW7t7f35'
        }
        entry_point = EntryPointSerializer.to_object(entry_point_json)
        self.assertEqual(entry_point.entry_point_type, EntryPoint.SIP)
        self.assertEqual(entry_point.uri, 'sip:123123')
        self.assertEqual(entry_point.label, 'label')
        self.assertEqual(entry_point.pin, 'rU9xzGHz')
        self.assertEqual(entry_point.access_code, 'sUhk4QPn')
        self.assertEqual(entry_point.meeting_code, 'sUhk4QPn')
        self.assertEqual(entry_point.passcode, 'YKa7m4D6')
        self.assertEqual(entry_point.password, 'JW7t7f35')

        entry_point_json = {
            'entryPointType': 'more',
            'uri': 'https://less.com',
            'password': 'JW7t7f35'
        }
        entry_point = EntryPointSerializer.to_object(entry_point_json)
        self.assertEqual(entry_point.entry_point_type, EntryPoint.MORE)
        self.assertEqual(entry_point.uri, 'https://less.com')
        self.assertIsNone(entry_point.label)
        self.assertIsNone(entry_point.pin)
        self.assertIsNone(entry_point.access_code)
        self.assertIsNone(entry_point.meeting_code)
        self.assertIsNone(entry_point.passcode)
        self.assertEqual(entry_point.password, 'JW7t7f35')


class TestConferenceSolution(TestCase):
    def test_init(self):
        conference_solution = ConferenceSolution(
            entry_points=EntryPoint(EntryPoint.VIDEO),
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )

        self.assertListEqual(conference_solution.entry_points, [EntryPoint(EntryPoint.VIDEO)])
        self.assertEqual(conference_solution.solution_type, SolutionType.HANGOUTS_MEET)
        self.assertEqual(conference_solution.name, 'Hangout')
        self.assertEqual(conference_solution.icon_uri, 'https://icon.com')
        self.assertEqual(conference_solution.conference_id, 'aaa-bbbb-ccc')
        self.assertEqual(conference_solution.signature, 'abc4efg12345')
        self.assertEqual(conference_solution.notes, 'important notes')

        conference_solution = ConferenceSolution(
            entry_points=[EntryPoint(EntryPoint.VIDEO)],
        )
        self.assertEqual(conference_solution.entry_points, [EntryPoint(EntryPoint.VIDEO)])

        conference_solution = ConferenceSolution(
            entry_points=[EntryPoint(EntryPoint.VIDEO),
                          EntryPoint(EntryPoint.PHONE)],
        )
        self.assertEqual(conference_solution.entry_points, [EntryPoint(EntryPoint.VIDEO),
                                                            EntryPoint(EntryPoint.PHONE)])

    def test_entry_point_types(self):
        with self.assertRaises(ValueError):
            ConferenceSolution(
                entry_points=[]
            )
        with self.assertRaises(ValueError):
            ConferenceSolution(
                entry_points=[
                    EntryPoint(EntryPoint.VIDEO),
                    EntryPoint(EntryPoint.VIDEO)
                ]
            )
        with self.assertRaises(ValueError):
            ConferenceSolution(
                entry_points=[
                    EntryPoint(EntryPoint.SIP),
                    EntryPoint(EntryPoint.SIP)
                ]
            )
        with self.assertRaises(ValueError):
            ConferenceSolution(
                entry_points=[
                    EntryPoint(EntryPoint.SIP),
                    EntryPoint(EntryPoint.MORE),
                    EntryPoint(EntryPoint.MORE)
                ]
            )
        with self.assertRaises(ValueError):
            # can't have only MORE entry point(s)
            ConferenceSolution(
                entry_points=[
                    EntryPoint(EntryPoint.MORE)
                ]
            )

    def test_eq(self):
        conference_solution = ConferenceSolution(
            entry_points=EntryPoint(EntryPoint.VIDEO),
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )
        self.assertFalse(conference_solution == 5)
        self.assertTrue(conference_solution == conference_solution)

    def test_repr_str(self):
        conference_solution = ConferenceSolution(
            entry_points=EntryPoint(EntryPoint.VIDEO),
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )

        self.assertEqual(conference_solution.__repr__(),
                         "<ConferenceSolution hangoutsMeet - [<EntryPoint video - 'None'>]>")
        self.assertEqual(conference_solution.__str__(),
                         "hangoutsMeet - [<EntryPoint video - 'None'>]")

        conference_solution = ConferenceSolution(
            entry_points=[EntryPoint(EntryPoint.VIDEO), EntryPoint(EntryPoint.SIP)],
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )

        self.assertEqual(conference_solution.__repr__(),
                         "<ConferenceSolution hangoutsMeet - [<EntryPoint video - 'None'>, <EntryPoint sip - 'None'>]>")
        self.assertEqual(conference_solution.__str__(),
                         "hangoutsMeet - [<EntryPoint video - 'None'>, <EntryPoint sip - 'None'>]")


class TestConferenceSolutionSerializer(TestCase):
    def test_to_json(self):
        conference_solution = ConferenceSolution(
            entry_points=EntryPoint(EntryPoint.VIDEO, uri='https://video.com'),
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )

        expected = {
            'entryPoints': [
                {
                    'entryPointType': 'video',
                    'uri': 'https://video.com',
                }
            ],
            'conferenceSolution': {
                'key': {
                    'type': 'hangoutsMeet'
                },
                'name': 'Hangout',
                'iconUri': 'https://icon.com'
            },
            'conferenceId': 'aaa-bbbb-ccc',
            'signature': 'abc4efg12345',
            'notes': 'important notes'
        }

        serializer = ConferenceSolutionSerializer(conference_solution)
        self.assertDictEqual(serializer.get_json(), expected)

        conference_solution = ConferenceSolution(
            entry_points=[
                EntryPoint(EntryPoint.VIDEO, uri='https://video.com'),
                EntryPoint(EntryPoint.PHONE, uri='+420000000000')
            ],
            solution_type=SolutionType.NAMED_HANGOUT,
        )

        expected = {
            'entryPoints': [
                {
                    'entryPointType': 'video',
                    'uri': 'https://video.com',
                },
                {
                    'entryPointType': 'phone',
                    'uri': '+420000000000',
                }
            ],
            'conferenceSolution': {
                'key': {
                    'type': 'eventNamedHangout'
                }
            }
        }

        self.assertDictEqual(ConferenceSolutionSerializer.to_json(conference_solution), expected)

    def test_to_object(self):
        conference_solution_json = {
            'entryPoints': [
                {
                    'entryPointType': 'video',
                    'uri': 'https://video.com',
                }
            ],
            'conferenceSolution': {
                'key': {
                    'type': 'hangoutsMeet'
                },
                'name': 'Hangout',
                'iconUri': 'https://icon.com'
            },
            'conferenceId': 'aaa-bbbb-ccc',
            'signature': 'abc4efg12345',
            'notes': 'important notes'
        }
        expected_conference_solution = ConferenceSolution(
            entry_points=EntryPoint(EntryPoint.VIDEO, uri='https://video.com'),
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )
        self.assertEqual(ConferenceSolutionSerializer.to_object(conference_solution_json),
                         expected_conference_solution)

        conference_solution_json = {
            'entryPoints': [
                {
                    'entryPointType': 'video',
                    'uri': 'https://video.com',
                },
                {
                    'entryPointType': 'phone',
                    'uri': '+420000000000',
                }
            ],
            'conferenceSolution': {
                'key': {
                    'type': 'eventNamedHangout'
                }
            }
        }
        expected_conference_solution = ConferenceSolution(
            entry_points=[
                EntryPoint(EntryPoint.VIDEO, uri='https://video.com'),
                EntryPoint(EntryPoint.PHONE, uri='+420000000000')
            ],
            solution_type=SolutionType.NAMED_HANGOUT,
        )
        self.assertEqual(ConferenceSolutionSerializer.to_object(conference_solution_json),
                         expected_conference_solution)

    def test_eq(self):
        conference_solution = ConferenceSolution(
            entry_points=EntryPoint(EntryPoint.VIDEO, uri='https://video.com'),
            solution_type=SolutionType.HANGOUTS_MEET,
            name='Hangout',
            icon_uri='https://icon.com',
            conference_id='aaa-bbbb-ccc',
            signature='abc4efg12345',
            notes='important notes'
        )
        self.assertFalse(conference_solution == 5)


class TestConferenceSolutionCreateRequest(TestCase):
    def test_init(self):
        cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            request_id='hello1234',
            conference_id='conference-id',
            signature='signature',
            notes='important notes'
        )
        self.assertEqual(cscr.solution_type, 'hangoutsMeet')
        self.assertEqual(cscr.request_id, 'hello1234')
        self.assertEqual(cscr.conference_id, 'conference-id')
        self.assertEqual(cscr.signature, 'signature')
        self.assertEqual(cscr.notes, 'important notes')

        cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
        )
        self.assertEqual(cscr.solution_type, 'hangoutsMeet')
        self.assertIsNotNone(cscr.request_id)

    def test_eq(self):
        cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            request_id='hello1234',
            conference_id='conference-id',
            signature='signature',
            notes='important notes'
        )
        self.assertFalse(cscr == 5)
        self.assertTrue(cscr == cscr)

    def test_repr_str(self):
        cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            request_id='hello1234',
            conference_id='conference-id',
            signature='signature',
            notes='important notes'
        )

        self.assertEqual(cscr.__repr__(), "<ConferenceSolutionCreateRequest hangoutsMeet - status:'None'>")
        self.assertEqual(cscr.__str__(), "hangoutsMeet - status:'None'")


class TestConferenceSolutionCreateRequestSerializer(TestCase):
    def test_to_json(self):
        cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            request_id='hello1234',
            conference_id='conference-id',
            signature='signature',
            notes='important notes',
            _status='pending'
        )
        expected = {
            'createRequest': {
                'requestId': 'hello1234',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'status': {
                    'statusCode': 'pending'
                }
            },
            'conferenceId': 'conference-id',
            'signature': 'signature',
            'notes': 'important notes'
        }
        serializer = ConferenceSolutionCreateRequestSerializer(cscr)
        self.assertDictEqual(serializer.get_json(), expected)

        cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            notes='important notes'
        )
        expected = {
            'createRequest': {
                'requestId': cscr.request_id,
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            },
            'notes': 'important notes'
        }
        self.assertDictEqual(ConferenceSolutionCreateRequestSerializer.to_json(cscr), expected)

    def test_to_object(self):
        cscr_json = {
            'createRequest': {
                'requestId': 'hello1234',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            },
            'conferenceId': 'conference-id',
            'signature': 'signature',
            'notes': 'important notes'
        }
        expected_cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            request_id='hello1234',
            conference_id='conference-id',
            signature='signature',
            notes='important notes'
        )
        self.assertEqual(ConferenceSolutionCreateRequestSerializer.to_object(cscr_json), expected_cscr)

        cscr_json = {
            'createRequest': {
                'requestId': 'hello1234',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            },
            'signature': 'signature'
        }
        expected_cscr = ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
            request_id='hello1234',
            signature='signature'
        )
        self.assertEqual(ConferenceSolutionCreateRequestSerializer.to_object(cscr_json), expected_cscr)
