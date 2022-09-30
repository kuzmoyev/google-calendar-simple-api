from .util import executable


class MockColorsRequests:
    """Emulates GoogleCalendar.service.colors()"""

    def __init__(self):
        self.test_colors = {
            'event': {
                '1': {'background': '#a4bdfc', 'foreground': '#1d1d1d'},
                '2': {'background': '#7ae7bf', 'foreground': '#1d1d1d'},
                '3': {'background': '#dbadff', 'foreground': '#1d1d1d'},
                '4': {'background': '#ff887c', 'foreground': '#1d1d1d'},
            },
            'calendar': {
                '1': {'background': '#ac725e', 'foreground': '#1d1d1d'},
                '2': {'background': '#d06b64', 'foreground': '#1d1d1d'},
                '3': {'background': '#f83a22', 'foreground': '#1d1d1d'},
                '4': {'background': '#fa573c', 'foreground': '#1d1d1d'},
                '5': {'background': '#fc573c', 'foreground': '#1d1d1d'},
            }
        }

    @executable
    def get(self, **_):
        """Emulates GoogleCalendar.service.colors().get().execute()"""
        return self.test_colors
