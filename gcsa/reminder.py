class Reminder:
    def __init__(self, method, minutes_before_start):
        self.method = method
        self.minutes_before_start = minutes_before_start


class EmailReminder(Reminder):
    def __init__(self, minutes_before_start=60):
        super().__init__('email', minutes_before_start)


class PopupReminder(Reminder):
    def __init__(self, minutes_before_start=30):
        super().__init__('popup', minutes_before_start)
