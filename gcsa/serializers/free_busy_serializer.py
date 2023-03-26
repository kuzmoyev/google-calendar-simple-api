from gcsa.free_busy import FreeBusy, TimeRange
from gcsa.serializers.base_serializer import BaseSerializer


class FreeBusySerializer(BaseSerializer):
    type_ = FreeBusy

    def __init__(self, free_busy):
        super().__init__(free_busy)

    @staticmethod
    def _to_json(free_busy: FreeBusy):
        """Isn't used as free busy data is read-only"""
        free_busy_json = {
            'calendars': {
                c: {
                    'busy': [
                        {
                            'start': start.isoformat(),
                            'end': end.isoformat(),
                        }
                        for start, end in free_busy.calendars.get(c, [])
                    ],
                    'errors': free_busy.calendars_errors.get(c, [])
                }
                for c in {**free_busy.calendars, **free_busy.calendars_errors}
            },
            'groups': {
                g: {
                    'calendars': free_busy.groups.get(g, []),
                    'errors': free_busy.groups_errors.get(g, [])
                }
                for g in {**free_busy.groups, **free_busy.groups_errors}
            },
            'timeMin': free_busy.time_min.isoformat(),
            'timeMax': free_busy.time_max.isoformat(),

        }
        return free_busy_json

    @staticmethod
    def _to_object(json_):
        time_min = FreeBusySerializer._get_datetime_from_string(json_['timeMin'])
        time_max = FreeBusySerializer._get_datetime_from_string(json_['timeMax'])
        groups_json = json_.get('groups')
        calendars_json = json_.get("calendars")

        if groups_json:
            groups = {gn: g['calendars'] for gn, g in groups_json.items() if g.get('calendars')}
            groups_errors = {gn: g['errors'] for gn, g in groups_json.items() if g.get('errors')}
        else:
            groups = {}
            groups_errors = {}

        if calendars_json:
            calendars = {
                cn: list(map(FreeBusySerializer._make_time_range, c['busy']))
                for cn, c in calendars_json.items() if c.get('busy') and not c.get('errors')
            }
            calendars_errors = {
                cn: c['errors']
                for cn, c in calendars_json.items() if c.get('errors')
            }
        else:
            calendars = {}
            calendars_errors = {}

        return FreeBusy(
            time_min=time_min,
            time_max=time_max,
            groups=groups,
            calendars=calendars,
            groups_errors=groups_errors,
            calendars_errors=calendars_errors
        )

    @staticmethod
    def _make_time_range(tp):
        return TimeRange(
            start=FreeBusySerializer._get_datetime_from_string(tp['start']),
            end=FreeBusySerializer._get_datetime_from_string(tp['end'])
        )
