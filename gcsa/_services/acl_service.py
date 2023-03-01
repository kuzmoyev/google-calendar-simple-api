from typing import Iterable, Union

from gcsa._services.base_service import BaseService
from gcsa.acl import AccessControlRule
from gcsa.serializers.acl_rule_serializer import ACLRuleSerializer


class ACLService(BaseService):
    """Access Control List management methods of the `GoogleCalendar`"""

    def get_acl_rules(
            self,
            calendar_id: str = None,
            show_deleted: bool = False
    ) -> Iterable[AccessControlRule]:
        """Returns the rules in the access control list for the calendar.

        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        :param show_deleted:
                Whether to include deleted ACLs in the result. Deleted ACLs are represented by role equal to "none".
                Deleted ACLs will always be included if syncToken is provided. Optional. The default is False.

        :return:
                Iterable of `AccessControlRule` objects
        """
        calendar_id = calendar_id or self.default_calendar
        yield from self._list_paginated(
            self.service.acl().list,
            serializer_cls=ACLRuleSerializer,
            calendarId=calendar_id,
            **{
                'showDeleted': show_deleted,
            }
        )

    def get_acl_rule(
            self,
            rule_id: str,
            calendar_id: str = None
    ) -> AccessControlRule:
        """Returns an access control rule

        :param rule_id:
                ACL rule identifier.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                The corresponding `AccessControlRule` object
        """
        calendar_id = calendar_id or self.default_calendar
        acl_rule_resource = self.service.acl().get(
            calendarId=calendar_id,
            ruleId=rule_id
        ).execute()
        return ACLRuleSerializer.to_object(acl_rule_resource)

    def add_acl_rule(
            self,
            acl_rule: AccessControlRule,
            send_notifications: bool = True,
            calendar_id: str = None
    ):
        """Adds access control rule

        :param acl_rule:
                AccessControlRule object.
        :param send_notifications:
                Whether to send notifications about the calendar sharing change. The default is True.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                Created access control rule with id.
        """
        calendar_id = calendar_id or self.default_calendar
        body = ACLRuleSerializer.to_json(acl_rule)
        acl_rule_json = self.service.acl().insert(
            calendarId=calendar_id,
            body=body,
            sendNotifications=send_notifications
        ).execute()
        return ACLRuleSerializer.to_object(acl_rule_json)

    def update_acl_rule(
            self,
            acl_rule: AccessControlRule,
            send_notifications: bool = True,
            calendar_id: str = None
    ):
        """Updates given access control rule

        :param acl_rule:
                AccessControlRule object.
        :param send_notifications:
                Whether to send notifications about the calendar sharing change. The default is True.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.

        :return:
                Updated access control rule.
        """
        calendar_id = calendar_id or self.default_calendar
        acl_id = self._get_resource_id(acl_rule)
        body = ACLRuleSerializer.to_json(acl_rule)
        acl_json = self.service.acl().update(
            calendarId=calendar_id,
            ruleId=acl_id,
            body=body,
            sendNotifications=send_notifications
        ).execute()
        return ACLRuleSerializer.to_object(acl_json)

    def delete_acl_rule(
            self,
            acl_rule: Union[AccessControlRule, str],
            calendar_id: str = None
    ):
        """Deletes access control rule.

        :param acl_rule:
                Access control rule's ID or `AccessControlRule` object with set `acl_id`.
        :param calendar_id:
                Calendar identifier. Default is `default_calendar` specified in `GoogleCalendar`.
                To retrieve calendar IDs call the :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list`.
                If you want to access the primary calendar of the currently logged-in user, use the "primary" keyword.
        """
        calendar_id = calendar_id or self.default_calendar
        acl_id = self._get_resource_id(acl_rule)

        self.service.acl().delete(
            calendarId=calendar_id,
            ruleId=acl_id
        ).execute()
