class EventBuilder:
    def __init__(self):
        pass

    @staticmethod
    def get_event_format():
        with open('event_format', 'r') as format_file:
            return format_file.read()
