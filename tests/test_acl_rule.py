from unittest import TestCase

from gcsa.acl import AccessControlRule, ACLRole, ACLScopeType
from gcsa.serializers.acl_rule_serializer import ACLRuleSerializer


class TestACLRule(TestCase):
    def test_repr_str(self):
        acl_rule = AccessControlRule(
            role=ACLRole.READER,
            scope_type=ACLScopeType.USER,
            scope_value='mail@gmail.com'
        )
        self.assertEqual(acl_rule.__repr__(), "<AccessControlRule mail@gmail.com - reader>")
        self.assertEqual(acl_rule.__str__(), "mail@gmail.com - reader")


class TestACLRuleSerializer(TestCase):
    def test_to_json(self):
        acl_rule = AccessControlRule(
            role=ACLRole.READER,
            scope_type=ACLScopeType.USER,
            acl_id='user:mail@gmail.com',
            scope_value='mail@gmail.com'
        )

        acl_rule_json = ACLRuleSerializer.to_json(acl_rule)
        self.assertEqual(acl_rule.role, acl_rule_json['role'])
        self.assertEqual(acl_rule.scope_type, acl_rule_json['scope']['type'])
        self.assertEqual(acl_rule.acl_id, acl_rule_json['id'])
        self.assertEqual(acl_rule.scope_value, acl_rule_json['scope']['value'])

    def test_to_object(self):
        acl_rule_json = {
            'id': 'user:mail@gmail.com',
            'scope': {
                'type': 'user',
                'value': 'mail@gmail.com'
            },
            'role': 'reader'
        }

        acl_rule = ACLRuleSerializer.to_object(acl_rule_json)

        self.assertEqual(acl_rule_json['role'], acl_rule.role)
        self.assertEqual(acl_rule_json['scope']['type'], acl_rule.scope_type)
        self.assertEqual(acl_rule_json['id'], acl_rule.acl_id)
        self.assertEqual(acl_rule_json['scope']['value'], acl_rule.scope_value)
