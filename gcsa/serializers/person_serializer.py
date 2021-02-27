from gcsa.person import Person
from gcsa.serializers.base_serializer import BaseSerializer


class PersonSerializer(BaseSerializer):
    type_ = Person

    def __init__(self, person):
        super().__init__(person)

    @staticmethod
    def _to_json(person: Person):
        data = {
            'email': person.email,
            'displayName': person.display_name
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def _to_object(json_person):
        return Person(
            email=json_person['email'],
            display_name=json_person.get('displayName', None),
            _id=json_person.get('id', None),
            _is_self=json_person.get('self', None)
        )
