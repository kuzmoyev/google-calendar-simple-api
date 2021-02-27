import dateutil.parser

from datetime import date, datetime

from tzlocal import get_localzone

from gcsa.event import Event
from .attachment_serializer import AttachmentSerializer
from .attendee_serializer import AttendeeSerializer
from .base_serializer import BaseSerializer
from .conference_serializer import ConferenceSolutionSerializer, ConferenceSolutionCreateRequestSerializer
from .person_serializer import PersonSerializer
from .reminder_serializer import ReminderSerializer
from ..conference import ConferenceSolution, ConferenceSolutionCreateRequest


class EventSerializer(BaseSerializer):
    type_ = Event

    def __init__(self, event):
        super().__init__(event)

    @classmethod
    def _to_json(cls, event: Event):
        data = {
            'summary': event.summary,
            'description': event.description,
            'location': event.location,
            'recurrence': event.recurrence,
            'colorId': event.color_id,
            'visibility': event.visibility,
            'attendees': [AttendeeSerializer.to_json(a) for a in event.attendees],
            'guestsCanInviteOthers': event.guests_can_invite_others,
            'guestsCanModify': event.guests_can_modify,
            'guestsCanSeeOtherGuests': event.guests_can_see_other_guests,
            'transparency': event.transparency,
            'reminders': {
                'useDefault': event.default_reminders,
                'overrides': [ReminderSerializer.to_json(r) for r in event.reminders]
            },
            'attachments': [AttachmentSerializer.to_json(a) for a in event.attachments],
            **event.other
        }

        if isinstance(event.start, datetime) and isinstance(event.end, datetime):
            data['start'] = {
                'dateTime': event.start.isoformat(),
                'timeZone': event.timezone
            }
            data['end'] = {
                'dateTime': event.end.isoformat(),
                'timeZone': event.timezone
            }
        elif isinstance(event.start, date) and isinstance(event.end, date):
            data['start'] = {'date': event.start.isoformat()}
            data['end'] = {'date': event.end.isoformat()}

        if event.default_reminders:
            data['reminders'] = {
                'useDefault': True
            }
        else:
            data['reminders'] = {
                'useDefault': False
            }
            if event.reminders:
                data['reminders']['overrides'] = [ReminderSerializer.to_json(r) for r in event.reminders]

        if event.conference_solution is not None:
            if isinstance(event.conference_solution, ConferenceSolution):
                data['conferenceData'] = ConferenceSolutionSerializer.to_json(event.conference_solution)
            elif isinstance(event.conference_solution, ConferenceSolutionCreateRequest):
                data['conferenceData'] = ConferenceSolutionCreateRequestSerializer.to_json(event.conference_solution)

        data = EventSerializer._remove_empty_values(data)

        return data

    @staticmethod
    def _to_object(json_event):
        timezone = None

        start = None
        start_data = json_event.pop('start', None)
        if start_data is not None:
            if 'date' in start_data:
                start = EventSerializer._get_datetime_from_string(start_data['date']).date()
            else:
                start = EventSerializer._get_datetime_from_string(start_data['dateTime'])
            timezone = start_data.get('timeZone', str(get_localzone()))

        end = None
        end_data = json_event.pop('end', None)
        if end_data is not None:
            if 'date' in end_data:
                end = EventSerializer._get_datetime_from_string(end_data['date']).date()
            else:
                end = EventSerializer._get_datetime_from_string(end_data['dateTime'])

        updated = json_event.pop('updated', None)
        if updated:
            updated = EventSerializer._get_datetime_from_string(updated)

        created = json_event.pop('created', None)
        if created:
            created = EventSerializer._get_datetime_from_string(created)

        attendees_json = json_event.pop('attendees', [])
        attendees = [AttendeeSerializer.to_object(a) for a in attendees_json]

        reminders_json = json_event.pop('reminders', {})
        reminders = [ReminderSerializer.to_object(r) for r in reminders_json.get('overrides', [])]

        attachments_json = json_event.pop('attachments', [])
        attachments = [AttachmentSerializer.to_object(a) for a in attachments_json]

        conference_data = json_event.pop('conferenceData', None)
        if conference_data is not None:
            create_request = conference_data.get('createRequest', {})
            if create_request is None or create_request.get('status', {}).get('statusCode', None) in (None, 'success'):
                conference_solution = ConferenceSolutionSerializer.to_object(conference_data)
            else:
                conference_solution = ConferenceSolutionCreateRequestSerializer.to_object(conference_data)
        else:
            conference_solution = None

        creator_data = json_event.pop('creator', None)
        if creator_data is not None:
            creator = PersonSerializer.to_object(creator_data)
        else:
            creator = None

        organizer_data = json_event.pop('organizer', None)
        if organizer_data is not None:
            organizer = PersonSerializer.to_object(organizer_data)
        else:
            organizer = None

        return Event(
            json_event.pop('summary', None),
            start=start,
            end=end,
            timezone=timezone,
            event_id=json_event.pop('id', None),
            description=json_event.pop('description', None),
            location=json_event.pop('location', None),
            recurrence=json_event.pop('recurrence', None),
            color_id=json_event.pop('colorId', None),
            visibility=json_event.pop('visibility', None),
            attendees=attendees,
            attachments=attachments,
            reminders=reminders,
            conference_solution=conference_solution,
            default_reminders=reminders_json.pop('useDefault', False),
            guests_can_invite_others=json_event.pop('guestsCanInviteOthers', True),
            guests_can_modify=json_event.pop('guestsCanModify', False),
            guests_can_see_other_guests=json_event.pop('guestsCanSeeOtherGuests', True),
            transparency=json_event.pop('transparency', None),
            _creator=creator,
            _organizer=organizer,
            _created=created,
            _updated=updated,
            _recurring_event_id=json_event.pop('recurringEventId', None),
            **json_event
        )

    @staticmethod
    def _get_datetime_from_string(s):
        return dateutil.parser.parse(s)
