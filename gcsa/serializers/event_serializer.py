import dateutil.parser

from datetime import date, datetime

from tzlocal import get_localzone

from gcsa.event import Event
from .attachment_serializer import AttachmentSerializer
from .base_serializer import BaseSerializer
from .gadget_serializer import GadgetSerializer
from .reminder_serializer import ReminderSerializer


class EventSerializer(BaseSerializer):
    type_ = Event

    def __init__(self, event):
        super().__init__(event)

    @staticmethod
    def to_json(event):
        if not isinstance(event, Event):
            raise TypeError('The event object must be Event, not {!r}.'.format(event.__class__.__name__))

        data = {
            "summary": event.summary,
            "description": event.description,
            "location": event.location,
            "recurrence": event.recurrence,
            "colorId": event.color_id,
            "visibility": event.visibility,
            "gadget": GadgetSerializer.to_json(event.gadget) if event.gadget else None,
            "reminders": {
                "useDefault": event.default_reminders,
                "overrides": [ReminderSerializer.to_json(r) for r in event.reminders]
            },
            "attachments": [AttachmentSerializer.to_json(a) for a in event.attachments],
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
                "useDefault": True
            }
        else:
            data['reminders'] = {
                "useDefault": False
            }
            if event.reminders:
                data['reminders']["overrides"] = [ReminderSerializer.to_json(r) for r in event.reminders]

        # Removes all None keys.
        data = {k: v for k, v in data.items() if v is not None}

        return data

    @staticmethod
    def to_object(json_event):
        BaseSerializer.assure_dict(json_event)

        start = None
        timezone = None
        start_data = json_event.get('start', None)
        if start_data is not None:
            if 'date' in start_data:
                start = EventSerializer._get_datetime_from_string(start_data['date']).date()
            else:
                start = EventSerializer._get_datetime_from_string(start_data['dateTime'])
            timezone = start_data.get('timeZone', str(get_localzone()))

        end = None
        end_data = json_event.get('end', None)
        if end_data is not None:
            if 'date' in end_data:
                end = EventSerializer._get_datetime_from_string(end_data['date']).date()
            else:
                end = EventSerializer._get_datetime_from_string(end_data['dateTime'])

        gadget_json = json_event.get('gadget', None)
        gadget = GadgetSerializer.to_object(gadget_json) if gadget_json else None

        reminders_json = json_event.get('reminders', {})
        reminders = [ReminderSerializer.to_object(r) for r in reminders_json.get('overrides', [])]

        attachments_json = json_event.get('attachments', [])
        attachments = [AttachmentSerializer.to_object(a) for a in attachments_json]

        return Event(
            json_event['summary'],
            start=start,
            end=end,
            timezone=timezone,
            event_id=json_event.get('id', None),
            description=json_event.get('description', None),
            location=json_event.get('location', None),
            recurrence=json_event.get('recurrence', None),
            color=json_event.get('colorId', None),
            visibility=json_event.get('visibility', None),
            gadget=gadget,
            attachments=attachments,
            reminders=reminders,
            default_reminders=reminders_json.get('useDefault', False),
            other=json_event
        )

    @staticmethod
    def _get_datetime_from_string(s):
        return dateutil.parser.parse(s)
