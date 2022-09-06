from typing import Callable, Type

from gcsa._services.authentication import AuthenticatedService


class BaseService(AuthenticatedService):
    def __init__(self, default_calendar, *args, **kwargs):
        """
        :param default_calendar:
                Users email address or name/id of the calendar. Default: primary calendar of the user

                If user's email or "primary" is specified, then primary calendar of the user is used.
                You don't need to specify this parameter in this case as it is a default behaviour.

                To use a different calendar you need to specify its id.
                Go to calendar's `settings and sharing` -> `Integrate calendar` -> `Calendar ID`.
        """
        super().__init__(*args, **kwargs)
        self.default_calendar = default_calendar

    @staticmethod
    def _list_paginated(
            request_method: Callable,
            serializer_cls: Type,
            **kwargs
    ):
        page_token = None
        while True:
            response_json = request_method(
                **kwargs,
                pageToken=page_token
            ).execute()
            for item_json in response_json['items']:
                yield serializer_cls(item_json).get_object()
            page_token = response_json.get('nextPageToken')
            if not page_token:
                break
