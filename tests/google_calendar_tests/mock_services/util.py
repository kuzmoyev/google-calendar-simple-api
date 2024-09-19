import webbrowser


class MockToken:
    def __init__(self, valid, refresh_token='refresh_token'):
        self.valid = valid
        self.expired = not valid
        self.refresh_token = refresh_token

    def refresh(self, _):
        self.valid = True
        self.expired = False


class MockAuthFlow:
    def __init__(self, has_browser=True):
        self.has_browser = has_browser

    def run_local_server(self, *args, open_browser=True, **kwargs):
        if not self.has_browser and open_browser:
            raise webbrowser.Error

        return MockToken(valid=True)


def executable(fn):
    """Decorator that stores data received from the function in object that returns that data when
    called its `execute` method. Emulates HttpRequest from googleapiclient."""

    class Executable:
        def __init__(self, data):
            self.data = data

        def execute(self):
            return self.data

    def wrapper(*args, **kwargs):
        data = fn(*args, **kwargs)
        return Executable(data)

    return wrapper


def within(dt, time_min, time_max):
    return time_min <= dt <= time_max


def time_range_within(tr, time_min, time_max):
    start, end = tr
    return within(start, time_min, time_max) and within(end, time_min, time_max)
