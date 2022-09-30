from gcsa._services.base_service import BaseService
from gcsa.serializers.settings_serializer import SettingsSerializer
from gcsa.settings import Settings


class SettingsService(BaseService):
    """Settings management methods of the `GoogleCalendar`"""

    def get_settings(self) -> Settings:
        """Returns user settings for the authenticated user."""
        settings_list = list(self._list_paginated(self.service.settings().list))
        settings_json = {s['id']: s['value'] for s in settings_list}
        return SettingsSerializer.to_object(settings_json)
