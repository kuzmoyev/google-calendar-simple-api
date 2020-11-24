from unittest import TestCase

from gcsa.attendee import Attendee, ResponseStatus
from gcsa.serializers.attendee_serializer import AttendeeSerializer


class TestAttendee(TestCase):
    def test_repr_str(self):
        attendee = Attendee(
            email='mail@gmail.com',
            display_name='Guest',
            comment='I do not know him',
            optional=True,
            additional_guests=2,
            _response_status=ResponseStatus.NEEDS_ACTION
        )
        self.assertEqual(attendee.__repr__(), "<Attendee 'mail@gmail.com' - response: 'needsAction'>")
        self.assertEqual(attendee.__str__(), "'mail@gmail.com' - response: 'needsAction'")


class TestAttendeeSerializer(TestCase):
    def test_to_json(self):
        attendee = Attendee(
            email='mail@gmail.com',
            display_name='Guest',
            comment='I do not know him',
            optional=True,
            additional_guests=2,
            _response_status=ResponseStatus.NEEDS_ACTION
        )

        attendee_json = AttendeeSerializer.to_json(attendee)

        self.assertEqual(attendee.email, attendee_json['email'])
        self.assertEqual(attendee.display_name, attendee_json['displayName'])
        self.assertEqual(attendee.comment, attendee_json['comment'])
        self.assertEqual(attendee.optional, attendee_json['optional'])
        self.assertNotIn('resource', attendee_json)
        self.assertEqual(attendee.additional_guests, attendee_json['additionalGuests'])
        self.assertEqual(attendee.response_status, attendee_json['responseStatus'])

    def test_to_object(self):
        attendee_json = {
            'email': 'mail2@gmail.com',
            'displayName': 'Guest2',
            'comment': 'I do not know him either',
            'optional': True,
            'resource': True,
            'additionalGuests': 1,
            'responseStatus': ResponseStatus.ACCEPTED
        }

        attendee = AttendeeSerializer.to_object(attendee_json)

        self.assertEqual(attendee_json['email'], attendee.email)
        self.assertEqual(attendee_json['displayName'], attendee.display_name)
        self.assertEqual(attendee_json['comment'], attendee.comment)
        self.assertEqual(attendee_json['optional'], attendee.optional)
        self.assertEqual(attendee_json['resource'], attendee.is_resource)
        self.assertEqual(attendee_json['additionalGuests'], attendee.additional_guests)
        self.assertEqual(attendee_json['responseStatus'], attendee.response_status)

        attendee_json_str = """{
            "email": "mail3@gmail.com",
            "displayName": "Guest3",
            "comment": "Who are these people?",
            "optional": true,
            "resource": false,
            "additionalGuests": 66,
            "responseStatus": "tentative"
        }"""

        serializer = AttendeeSerializer(attendee_json_str)
        attendee = serializer.get_object()

        self.assertEqual(attendee.email, "mail3@gmail.com")
        self.assertEqual(attendee.display_name, "Guest3")
        self.assertEqual(attendee.comment, "Who are these people?")
        self.assertEqual(attendee.optional, True)
        self.assertEqual(attendee.is_resource, False)
        self.assertEqual(attendee.additional_guests, 66)
        self.assertEqual(attendee.response_status, "tentative")
