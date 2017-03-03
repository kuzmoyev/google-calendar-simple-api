from src.event import Event
from json import loads


class EventSerializer:
    def __init__(self, event):
        if isinstance(event, Event):
            self.data = self.event2json(event)
        elif isinstance(event, str):
            self.data = loads(event)
        elif isinstance(event, dict):
            self.data = event
        else:
            raise TypeError('the event object must be Event, str or dict, not {!r}'.format(event.__class__.__name__))

    def get_event(self):
        return self.json2event(self.data)

    def get_json(self):
        return self.data

    @staticmethod
    def event2json(event):
        if not isinstance(event, Event):
            raise TypeError('the event object must be Event, not {!r}'.format(event.__class__.__name__))

    @staticmethod
    def json2event(json):
        if not (isinstance(json, str) or isinstance(json, dict)):
            raise TypeError('the event object must be str or dict, not {!r}'.format(json.__class__.__name__))

        if isinstance(json, str):
            json = loads(json)
