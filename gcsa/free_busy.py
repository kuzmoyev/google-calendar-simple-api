import json
from collections import namedtuple
from datetime import datetime
from typing import Dict, List

TimeRange = namedtuple('TimeRange', ('start', 'end'))


class FreeBusy:
    def __init__(
            self,
            *,
            time_min: datetime,
            time_max: datetime,
            groups: Dict[str, List[str]],
            calendars: Dict[str, List[TimeRange]],
            groups_errors: Dict = None,
            calendars_errors: Dict = None,
    ):
        self.time_min = time_min
        self.time_max = time_max
        self.groups = groups
        self.calendars = calendars
        self.groups_errors = groups_errors or {}
        self.calendars_errors = calendars_errors or {}

    def __str__(self):
        return '<FreeBusy {} - {}>'.format(self.time_min, self.time_max)

    def __repr__(self):
        return self.__str__()


class FreeBusyQueryError(Exception):
    def __init__(self, groups_errors, calendars_errors):
        message = '\n'
        if groups_errors:
            message += f'Groups errors: {json.dumps(groups_errors, indent=4)}'
        if calendars_errors:
            message += f'Calendars errors: {json.dumps(calendars_errors, indent=4)}'
        super().__init__(message)
        self.groups_errors = groups_errors
        self.calendars_errors = calendars_errors
