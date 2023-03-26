from datetime import date, datetime
from typing import Union, List

from beautiful_date import BeautifulDate
from dateutil.relativedelta import relativedelta
from tzlocal import get_localzone_name

from gcsa._services.base_service import BaseService
from gcsa.free_busy import FreeBusy, FreeBusyQueryError
from gcsa.serializers.free_busy_serializer import FreeBusySerializer
from gcsa.util.date_time_util import to_localized_iso


class FreeBusyService(BaseService):
    def get_free_busy(
            self,
            resource_ids: Union[str, List[str]] = None,
            *,
            time_min: Union[date, datetime, BeautifulDate] = None,
            time_max: Union[date, datetime, BeautifulDate] = None,
            timezone: str = get_localzone_name(),
            group_expansion_max: int = None,
            calendar_expansion_max: int = None,
            ignore_errors: bool = False
    ) -> FreeBusy:
        """Returns free/busy information for a set of calendars and/or groups.

        :param resource_ids:
                Identifier or list of identifiers of calendar(s) and/or group(s).
                Default is `default_calendar` specified in `GoogleCalendar`.
        :param time_min:
                The start of the interval for the query.
        :param time_max:
                The end of the interval for the query.
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param group_expansion_max:
                Maximal number of calendar identifiers to be provided for a single group.
                An error is returned for a group with more members than this value.
                Maximum value is 100.
        :param calendar_expansion_max:
                Maximal number of calendars for which FreeBusy information is to be provided.
                Maximum value is 50.
        :param ignore_errors:
                Whether errors related to calendars and/or groups should be ignored.
                If `False` :py:class:`~gcsa.free_busy.FreeBusyQueryError` is raised in case of query related errors.
                If `True`, related errors are stored in the resulting :py:class:`~gcsa.free_busy.FreeBusy` object.
                Default is `False`.
                Note, request related errors (e.x. authentication error) will not be ignored regardless of
                the `ignore_errors` value.

        :return:
                :py:class:`~gcsa.free_busy.FreeBusy` object.
        """

        time_min = time_min or datetime.now()
        time_max = time_max or time_min + relativedelta(weeks=2)

        time_min = to_localized_iso(time_min, timezone)
        time_max = to_localized_iso(time_max, timezone)

        if resource_ids is None:
            resource_ids = [self.default_calendar]
        elif not isinstance(resource_ids, (list, tuple, set)):
            resource_ids = [resource_ids]

        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "timeZone": timezone,
            "groupExpansionMax": group_expansion_max,
            "calendarExpansionMax": calendar_expansion_max,
            "items": [
                {
                    "id": r_id
                } for r_id in resource_ids
            ]
        }

        free_busy_json = self.service.freebusy().query(body=body).execute()
        free_busy = FreeBusySerializer.to_object(free_busy_json)
        if not ignore_errors and (free_busy.groups_errors or free_busy.calendars_errors):
            raise FreeBusyQueryError(groups_errors=free_busy.groups_errors,
                                     calendars_errors=free_busy.calendars_errors)

        return free_busy
