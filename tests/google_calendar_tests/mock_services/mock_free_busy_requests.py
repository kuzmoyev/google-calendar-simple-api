from typing import List

import dateutil.parser
from beautiful_date import D, days, hours

from gcsa.free_busy import FreeBusy, TimeRange
from gcsa.serializers.free_busy_serializer import FreeBusySerializer
from gcsa.util.date_time_util import ensure_localisation
from .util import executable, time_range_within

NOT_FOUND_ERROR = [
    {
        "domain": "global",
        "reason": "notFound"
    }
]


class MockFreeBusyRequests:
    """Emulates GoogleCalendar.service.freebusy()"""

    def __init__(self):
        now = ensure_localisation(D.now())
        self.groups = {
            'group1': ['primary', 'calendar2'],
            'group2': ['calendar3', 'calendar4']
        }
        self.calendars = {
            'primary': [
                TimeRange(now - 1 * days, now - 1 * days + 1 * hours),
                TimeRange(now + 1 * hours, now + 2 * hours),
                TimeRange(now + 1 * days + 1 * hours, now + 1 * days + 2 * hours),
                TimeRange(now + 15 * days + 1 * hours, now + 15 * days + 2 * hours),
            ],
            'calendar2': [
                TimeRange(now - 1 * days, now - 1 * days + 1 * hours),
                TimeRange(now + 1 * hours, now + 2 * hours),
                TimeRange(now + 1 * days + 1 * hours, now + 1 * days + 2 * hours),
                TimeRange(now + 15 * days + 1 * hours, now + 15 * days + 2 * hours),
            ],
            'calendar3': [
                TimeRange(now - 1 * days, now - 1 * days + 1 * hours),
                TimeRange(now + 1 * hours, now + 2 * hours),
                TimeRange(now + 1 * days + 1 * hours, now + 1 * days + 2 * hours),
                TimeRange(now + 15 * days + 1 * hours, now + 15 * days + 2 * hours),
            ],
            'calendar4': [
                TimeRange(now - 1 * days, now - 1 * days + 1 * hours),
                TimeRange(now + 1 * hours, now + 2 * hours),
                TimeRange(now + 1 * days + 1 * hours, now + 1 * days + 2 * hours),
                TimeRange(now + 15 * days + 1 * hours, now + 15 * days + 2 * hours),
            ],
        }

    @executable
    def query(self, body):
        """Emulates GoogleCalendar.service.freebusy().query().execute()"""
        time_min = dateutil.parser.parse(body['timeMin'])
        time_max = dateutil.parser.parse(body['timeMax'])
        items = body['items']

        request_groups = [i['id'] for i in items if i['id'].startswith('group')]
        request_calendars = {i['id'] for i in items if not i['id'].startswith('group')}

        groups = {gn: g for gn, g in self.groups.items() if gn in request_groups}
        group_calendars = set(c for g in groups.values() for c in g)
        calendars = {
            cn: self._filter_ranges(c, time_min, time_max)
            for cn, c in self.calendars.items()
            if cn in request_calendars | group_calendars
        }

        calendars_errors = {c: NOT_FOUND_ERROR for c in request_calendars if c not in calendars}
        groups_errors = {g: NOT_FOUND_ERROR for g in request_groups if g not in groups}

        fb_json = FreeBusySerializer.to_json(FreeBusy(
            time_min=time_min,
            time_max=time_max,
            groups=groups,
            calendars=calendars,
            calendars_errors=calendars_errors,
            groups_errors=groups_errors
        ))
        return fb_json

    @staticmethod
    def _filter_ranges(time_ranges: List[TimeRange], time_min, time_max):
        return [tr for tr in time_ranges if time_range_within(tr, time_min, time_max)]
