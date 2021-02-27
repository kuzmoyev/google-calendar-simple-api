from unittest import TestCase

from gcsa.person import Person
from gcsa.serializers.person_serializer import PersonSerializer


class TestPerson(TestCase):
    def test_repr_str(self):
        person = Person(
            email='mail@gmail.com',
            display_name='Guest',
            _id='123123',
            _is_self=False
        )
        self.assertEqual(person.__repr__(), "<Person 'mail@gmail.com' - 'Guest'>")
        self.assertEqual(person.__str__(), "'mail@gmail.com' - 'Guest'")


class TestPersonSerializer(TestCase):
    def test_to_json(self):
        person = Person(
            email='mail@gmail.com',
            display_name='Organizer'
        )

        person_json = PersonSerializer(person).get_json()

        self.assertEqual(person.email, person_json['email'])
        self.assertEqual(person.display_name, person_json['displayName'])

    def test_to_object(self):
        person_json = {
            'email': 'mail2@gmail.com',
            'displayName': 'Creator',
            'id': '123123',
            'self': False
        }

        person = PersonSerializer.to_object(person_json)

        self.assertEqual(person_json['email'], person.email)
        self.assertEqual(person_json['displayName'], person.display_name)
        self.assertEqual(person_json['id'], person.id_)
        self.assertEqual(person_json['self'], person.is_self)
