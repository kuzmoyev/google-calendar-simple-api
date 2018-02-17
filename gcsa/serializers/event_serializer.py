import dateutil.parser

from gcsa.event import Event
from json import loads, dumps
from datetime import date, datetime


class EventSerializer:
    def __init__(self, event):
        if isinstance(event, Event):
            self.data = self.event2json(event)
        elif isinstance(event, str):
            self.data = loads(event)
        elif isinstance(event, dict):
            self.data = event
        else:
            raise TypeError('The event object must be Event, str or dict, not {!r}'.format(event.__class__.__name__))

    def get_event(self):
        return self.json2event(self.data)

    def get_json(self):
        return self.data

    @staticmethod
    def event2json(event):
        if not isinstance(event, Event):
            raise TypeError('The event object must be Event, not {!r}'.format(event.__class__.__name__))

        data = {
            "summary": event.summary,
            "description": event.description,
            "location": event.location,
            "start": {
                "timeZone": event.timezone
            },
            "end": {
                "timeZone": event.timezone
            },
            "recurrence": event.recurrence,
            "colorId": event.colorId,
            "visibility": event.visibility,
            "reminders": {
                "useDefault": event.default_reminders,
                "overrides": event.reminders
            },
            "attachments": event.attachments
        }

        if isinstance(event.start, date) and isinstance(event.end, date):
            data['start']['date'] = event.start.isoformat()
            data['end']['date'] = event.end.isoformat()
        elif isinstance(event.start, datetime) and isinstance(event.end, datetime):
            data['start']['datetime'] = event.start.isoformat()
            data['end']['datetime'] = event.end.isoformat()

        return dumps(data)

    @staticmethod
    def json2event(json):
        if not isinstance(json, (str, dict)):
            raise TypeError('The json object must be str or dict, not {!r}'.format(json.__class__.__name__))

        if isinstance(json, str):
            json = loads(json)

        start = None
        timzone = None
        start_data = json.pop('start', None)
        if start_data is not None:
            if 'date' in start_data:
                start = EventSerializer._get_datetime_from_string(start_data['date']).date()
            else:
                start = EventSerializer._get_datetime_from_string(start_data['dateTime'])
            timzone = start_data.pop('timeZone', None)

        end = None
        end_data = json.pop('end', None)
        if end_data is not None:
            if 'date' in end_data:
                end = EventSerializer._get_datetime_from_string(end_data['date']).date()
            else:
                end = EventSerializer._get_datetime_from_string(end_data['dateTime'])

        reminders = json.pop('reminders', {})

        event = Event(
            start=start,
            end=end,
            timezone=timzone,
            event_id=json.pop('id', None),
            summary=json.pop('summary', None),
            description=json.pop('description', None),
            location=json.pop('location', None),
            recurrence=json.pop('recurrence', None),
            color=json.pop('colorId', None),
            visibility=json.pop('visibility', None),
            gadget=json.pop('gadget', None),
            attachments=json.pop('attachments', None),
            reminders=reminders.pop('overrides', None),
            default_reminders=reminders.pop('useDefault', False),
            other=json
        )
        
        return event

    @staticmethod
    def _get_datetime_from_string(s):
        d = dateutil.parser.parse(s)
        return d
