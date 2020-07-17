from gcsa.attendee import Attendee
from gcsa.serializers.base_serializer import BaseSerializer


class AttendeeSerializer(BaseSerializer):
    type_ = Attendee

    def __init__(self, attendee):
        super().__init__(attendee)

    @staticmethod
    def to_json(attendee):
        data = {
            'email': attendee.email,
            'displayName': attendee.display_name,
            'comment': attendee.comment,
            'optional': attendee.optional,
            'resource': attendee.is_resource,
            'additionalGuests': attendee.additional_guests,
            'responseStatus': attendee.response_status
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def to_object(json_attendee):
        json_attendee = BaseSerializer.assure_dict(json_attendee)

        return Attendee(
            email=json_attendee['email'],
            display_name=json_attendee.get('displayName'),
            comment=json_attendee.get('comment'),
            optional=json_attendee.get('optional'),
            is_resource=json_attendee.get('resource'),
            additional_guests=json_attendee.get('additionalGuests'),
            response_status=json_attendee.get('responseStatus')
        )
