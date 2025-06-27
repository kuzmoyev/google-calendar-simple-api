from datetime import time, datetime
from typing import Optional

from beautiful_date import days

from gcsa.util.date_time_util import DateOrDatetime


class Reminder:
    def __init__(
            self,
            method: str,
            minutes_before_start: Optional[int] = None,
            days_before: Optional[int] = None,
            at: Optional[time] = None
    ):
        """Represents base reminder object

        Provide `minutes_before_start` to create "relative" reminder.
        Provide `days_before` and `at` to create "absolute" reminder.

        :param method:
                Method of the reminder. Possible values: email or popup
        :param minutes_before_start:
                Minutes before reminder
        :param days_before:
                Days before reminder
        :param at:
                Specific time for a reminder
        """
        # Nothing was provided
        if minutes_before_start is None and days_before is None and at is None:
            raise ValueError("Relative reminder needs 'minutes_before_start'. "
                             "Absolute reminder 'days_before' and 'at' set. "
                             "None of them were provided.")

        # Both minutes_before_start and days_before/at were provided
        if minutes_before_start is not None and (days_before is not None or at is not None):
            raise ValueError("Only minutes_before_start or days_before/at can be specified.")

        # Only one of days_before and at was provided
        if (days_before is None) != (at is None):
            raise ValueError(f'Both "days_before" and "at" values need to be set '
                             f'when using absolute time for a reminder. '
                             f'Provided days_before={days_before} and at={at}.')

        self.method = method
        self.minutes_before_start = minutes_before_start
        self.days_before = days_before
        self.at = at

    def __eq__(self, other):
        return (
                isinstance(other, Reminder)
                and self.method == other.method
                and self.minutes_before_start == other.minutes_before_start
                and self.days_before == other.days_before
                and self.at == other.at
        )

    def __str__(self):
        if self.minutes_before_start is not None:
            return '{} - minutes_before_start:{}'.format(self.__class__.__name__, self.minutes_before_start)
        else:
            return '{} - {} days before at {}'.format(self.__class__.__name__, self.days_before, self.at)

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def convert_to_relative(self, start: DateOrDatetime) -> 'Reminder':
        """Converts absolute reminder (with set `days_before` and `at`) to relative (with set `minutes_before_start`)
         relative to `start` date/datetime. Returns self if `minutes_before_start` is already set.
         """
        if self.minutes_before_start is not None:
            return self

        if self.days_before is None or self.at is None:
            raise ValueError(f'Both "days_before" and "at" values need to be set '
                             f'when using absolute time for a reminder. '
                             f'Provided days_before={self.days_before} and at={self.at}.')

        tzinfo = start.tzinfo if isinstance(start, datetime) else None
        start_of_the_day = datetime.combine(start, datetime.min.time(), tzinfo=tzinfo)

        reminder_tzinfo = self.at.tzinfo or tzinfo
        reminder_time = datetime.combine(start_of_the_day - self.days_before * days, self.at, tzinfo=reminder_tzinfo)

        if isinstance(start, datetime):
            minutes_before_start = int((start - reminder_time).total_seconds() / 60)
        else:
            minutes_before_start = int((start_of_the_day - reminder_time).total_seconds() / 60)

        return Reminder(
            method=self.method,
            minutes_before_start=minutes_before_start
        )


class EmailReminder(Reminder):
    def __init__(
            self,
            minutes_before_start: Optional[int] = None,
            days_before: Optional[int] = None,
            at: Optional[time] = None
    ):
        """Represents email reminder object

        Provide `minutes_before_start` to create "relative" reminder.
        Provide `days_before` and `at` to create "absolute" reminder.

        :param minutes_before_start:
                Minutes before reminder
        :param days_before:
                Days before reminder
        :param at:
                Specific time for a reminder
        """
        if not days_before and not at and not minutes_before_start:
            minutes_before_start = 60
        super().__init__('email', minutes_before_start, days_before, at)


class PopupReminder(Reminder):
    def __init__(
            self,
            minutes_before_start: Optional[int] = None,
            days_before: Optional[int] = None,
            at: Optional[time] = None
    ):
        """Represents popup reminder object

        Provide `minutes_before_start` to create "relative" reminder.
        Provide `days_before` and `at` to create "absolute" reminder.

        :param minutes_before_start:
                Minutes before reminder
        :param days_before:
                Days before reminder
        :param at:
                Specific time for a reminder
        """
        if not days_before and not at and not minutes_before_start:
            minutes_before_start = 30
        super().__init__('popup', minutes_before_start, days_before, at)
