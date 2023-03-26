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
        """Represents free/busy information for a given calendar(s) and/or group(s)

        :param time_min:
                The start of the interval.
        :param time_max:
                The end of the interval.
        :param groups:
                Expansion of groups.
                Dictionary that maps the name of the group to the list of calendars that are members of this group.
        :param calendars:
                Free/busy information for calendars.
                Dictionary that maps calendar id to the list of time ranges during which this calendar should be
                regarded as busy.
        :param groups_errors:
                Optional error(s) (if computation for the group failed).
                Dictionary that maps the name of the group to the list of errors.
        :param calendars_errors:
                Optional error(s) (if computation for the calendar failed).
                Dictionary that maps calendar id to the list of errors.


        .. note:: Errors have the following format:

            .. code-block::

                {
                  "domain": "<domain>",
                  "reason": "<reason>"
                }

            Some possible values for "reason" are:

             * "groupTooBig" - The group of users requested is too large for a single query.
             * "tooManyCalendarsRequested" - The number of calendars requested is too large for a single query.
             * "notFound" - The requested resource was not found.
             * "internalError" - The API service has encountered an internal error.

            Additional error types may be added in the future.
        """
        self.time_min = time_min
        self.time_max = time_max
        self.groups = groups
        self.calendars = calendars
        self.groups_errors = groups_errors or {}
        self.calendars_errors = calendars_errors or {}

    def __iter__(self):
        """
        :returns:
                list of 'TimeRange's during which this calendar should be regarded as busy.
        :raises:
                ValueError if requested all requested calendars have errors
                or more than one calendar has been requested.
        """
        if len(self.calendars) == 0:
            raise ValueError("No free/busy information has been received. "
                             "Check the 'calendars_errors' and 'groups_errors' fields.")
        if len(self.calendars) > 1 or len(self.calendars_errors) > 0:
            raise ValueError("Can't iterate over FreeBusy objects directly when more than one calendars were requested."
                             "Use 'calendars' field instead to get free/busy information of the specific calendar.")
        return iter(next(iter(self.calendars.values())))

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
