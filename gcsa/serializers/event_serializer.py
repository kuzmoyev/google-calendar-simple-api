import dateutil.parser

import json
from datetime import date, datetime

from event import Event


class EventSerializer:
    def __init__(self, event):
        if isinstance(event, Event):
            self.data = self.event2json(event)
        elif isinstance(event, str):
            self.data = json.loads(event)
        elif isinstance(event, dict):
            self.data = event
        else:
            raise TypeError('The event object must be Event, str or dict, not {!r}.'.format(event.__class__.__name__))

    def get_event(self):
        return self.json2event(self.data)

    def get_json(self):
        return self.data

    @staticmethod
    def event2json(event):
        if not isinstance(event, Event):
            raise TypeError('The event object must be Event, not {!r}.'.format(event.__class__.__name__))

        data = {
            "summary": event.summary,
            "description": event.description,
            "location": event.location,
            "start": {},
            "end": {},
            "recurrence": event.recurrence,
            "colorId": event.colorId,
            "visibility": event.visibility,
            "reminders": {
                "useDefault": event.default_reminders,
                "overrides": event.reminders
            },
            "attachments": event.attachments,
            **event.other
        }

        if isinstance(event.start, datetime) and isinstance(event.end, datetime):
            data['start']['dateTime'] = event.start.isoformat()
            data['end']['dateTime'] = event.end.isoformat()
        elif isinstance(event.start, date) and isinstance(event.end, date):
            data['start']['date'] = event.start.isoformat()
            data['end']['date'] = event.end.isoformat()

        # Removes all None keys.
        data = {k: v for k, v in data.items() if v is not None}

        return data

    @staticmethod
    def json2event(json_event):
        if not isinstance(json_event, (str, dict)):
            raise TypeError('The json object must be str or dict, not {!r}'.format(json_event.__class__.__name__))

        if isinstance(json_event, str):
            json_event = json.loads(json_event)

        start = None
        timezone = None
        start_data = json_event.pop('start', None)
        if start_data is not None:
            if 'date' in start_data:
                start = EventSerializer._get_datetime_from_string(start_data['date']).date()
            else:
                start = EventSerializer._get_datetime_from_string(start_data['dateTime'])
            timezone = start_data.pop('timeZone', None)

        end = None
        end_data = json_event.pop('end', None)
        if end_data is not None:
            if 'date' in end_data:
                end = EventSerializer._get_datetime_from_string(end_data['date']).date()
            else:
                end = EventSerializer._get_datetime_from_string(end_data['dateTime'])

        reminders = json_event.pop('reminders', {})

        event = Event(
            start=start,
            end=end,
            timezone=timezone,
            event_id=json_event.pop('id', None),
            summary=json_event.pop('summary', None),
            description=json_event.pop('description', None),
            location=json_event.pop('location', None),
            recurrence=json_event.pop('recurrence', None),
            color=json_event.pop('colorId', None),
            visibility=json_event.pop('visibility', None),
            gadget=json_event.pop('gadget', None),
            attachments=json_event.pop('attachments', None),
            reminders=reminders.pop('overrides', None),
            default_reminders=reminders.pop('useDefault', False),
            other=json_event
        )

        return event

    @staticmethod
    def _get_datetime_from_string(s):
        return dateutil.parser.parse(s)
