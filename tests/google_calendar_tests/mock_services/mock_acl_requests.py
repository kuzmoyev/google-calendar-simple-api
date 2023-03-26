from gcsa.acl import AccessControlRule, ACLRole, ACLScopeType
from gcsa.serializers.acl_rule_serializer import ACLRuleSerializer
from .util import executable


class MockACLRequests:
    """Emulates GoogleCalendar.service.acl()"""
    ACL_RULES_PER_PAGE = 3

    def __init__(self):
        self.test_acl_rules = []
        for i in range(4):
            self.test_acl_rules.append(
                AccessControlRule(
                    role=ACLRole.READER,
                    scope_type=ACLScopeType.USER,
                    acl_id=f'user:mail{i}@gmail.com',
                    scope_value=f'mail{i}@gmail.com'
                )
            )
            self.test_acl_rules.append(
                AccessControlRule(
                    role=ACLRole.READER,
                    scope_type=ACLScopeType.GROUP,
                    acl_id=f'group:group-mail{i}@gmail.com',
                    scope_value=f'group-mail{i}@gmail.com'
                )
            )

    @property
    def test_acl_rules_by_id(self):
        return {c.id: c for c in self.test_acl_rules}

    @executable
    def list(self, pageToken, **_):
        """Emulates GoogleCalendar.service.acl().list().execute()"""
        page = pageToken or 0  # page number in this case
        page_acl_rules = self.test_acl_rules[page * self.ACL_RULES_PER_PAGE:(page + 1) * self.ACL_RULES_PER_PAGE]
        next_page = page + 1 if (page + 1) * self.ACL_RULES_PER_PAGE < len(self.test_acl_rules) else None

        return {
            'items': [
                ACLRuleSerializer.to_json(c)
                for c in page_acl_rules
            ],
            'nextPageToken': next_page
        }

    @executable
    def get(self, calendarId, ruleId):
        """Emulates GoogleCalendar.service.acl().get().execute()"""
        try:
            return ACLRuleSerializer.to_json(self.test_acl_rules_by_id[ruleId])
        except KeyError:
            # shouldn't get here in tests
            raise ValueError(f'ACLRule with id {ruleId} does not exist')

    @executable
    def insert(self, calendarId, body, sendNotifications):
        """Emulates GoogleCalendar.service.acl().insert().execute()"""
        acl_rule: AccessControlRule = ACLRuleSerializer.to_object(body)
        acl_rule.acl_id = f'{acl_rule.scope_type}:{acl_rule.scope_value}'
        self.test_acl_rules.append(acl_rule)
        return ACLRuleSerializer.to_json(acl_rule)

    @executable
    def update(self, calendarId, ruleId, body, sendNotifications):
        """Emulates GoogleCalendar.service.acl().update().execute()"""
        acl_rule = ACLRuleSerializer.to_object(body)
        for i in range(len(self.test_acl_rules)):
            if ruleId == self.test_acl_rules[i].id:
                self.test_acl_rules[i] = acl_rule
                return ACLRuleSerializer.to_json(acl_rule)

        # shouldn't get here in tests
        raise ValueError(f'ACL rule with id {ruleId} does not exist')

    @executable
    def delete(self, calendarId, ruleId):
        """Emulates GoogleCalendar.service.acl().delete().execute()"""
        self.test_acl_rules = [c for c in self.test_acl_rules if c.id != ruleId]
