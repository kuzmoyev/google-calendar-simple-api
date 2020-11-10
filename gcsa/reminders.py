class Reminder:
    def __init__(self, method, minutes_before_start):
        """Represents base reminder object

        :param method:
                Method of the reminder. Possible values: email or popup
        :param minutes_before_start:
                Minutes before reminder
        """
        self.method = method
        self.minutes_before_start = minutes_before_start

    def __eq__(self, other):
        return isinstance(other, Reminder) \
               and self.method == other.method \
               and self.minutes_before_start == other.minutes_before_start


class EmailReminder(Reminder):
    def __init__(self, minutes_before_start=60):
        """Represents email reminder object

        :param minutes_before_start:
                Minutes before reminder
        """
        super().__init__('email', minutes_before_start)


class PopupReminder(Reminder):
    def __init__(self, minutes_before_start=30):
        """Represents popup reminder object

        :param minutes_before_start:
                Minutes before reminder
        """
        super().__init__('popup', minutes_before_start)
