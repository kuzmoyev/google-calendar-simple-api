from gcsa.acl import AccessControlRule, ACLRole, ACLScopeType
from tests.google_calendar_tests.test_case_with_mocked_service import TestCaseWithMockedService


class TestACLService(TestCaseWithMockedService):
    def test_get_access_control_list(self):
        acl_rules = list(self.gc.get_acl_rules())
        self.assertEqual(len(acl_rules), 8)

    def test_get_acl_rule(self):
        acl_rule = self.gc.get_acl_rule(rule_id='user:mail2@gmail.com')

        self.assertEqual(acl_rule.acl_id, 'user:mail2@gmail.com')
        self.assertEqual(acl_rule.role, 'reader')
        self.assertEqual(acl_rule.scope_type, 'user')
        self.assertEqual(acl_rule.scope_value, 'mail2@gmail.com')

    def test_add_acl_rule(self):
        acl_rule = AccessControlRule(
            role=ACLRole.WRITER,
            scope_type=ACLScopeType.DOMAIN,
            scope_value='test.com'
        )

        acl_rule = self.gc.add_acl_rule(acl_rule)

        self.assertEqual(acl_rule.acl_id, 'domain:test.com')
        self.assertEqual(acl_rule.role, 'writer')
        self.assertEqual(acl_rule.scope_type, 'domain')
        self.assertEqual(acl_rule.scope_value, 'test.com')

    def test_update_acl_rule(self):
        acl_rule = self.gc.get_acl_rule(rule_id='user:mail2@gmail.com')
        acl_rule.role = ACLRole.FREE_BUSY_READER

        self.gc.update_acl_rule(acl_rule)
        acl_rule = self.gc.get_acl_rule(rule_id='user:mail2@gmail.com')

        self.assertEqual(acl_rule.acl_id, 'user:mail2@gmail.com')
        self.assertEqual(acl_rule.role, 'freeBusyReader')
        self.assertEqual(acl_rule.scope_type, 'user')
        self.assertEqual(acl_rule.scope_value, 'mail2@gmail.com')

    def test_delete_acl_rule(self):
        self.gc.delete_acl_rule(acl_rule='user:mail2@gmail.com')
        self.gc.delete_acl_rule(
            acl_rule=AccessControlRule(
                role=ACLRole.READER,
                scope_type=ACLScopeType.GROUP,
                acl_id='group:group-mail1@gmail.com',
                scope_value='group-mail1@gmail.com'
            )
        )
        deleted_ids = ('user:mail2@gmail.com', 'group:group-mail1@gmail.com')

        acl_rules = list(self.gc.get_acl_rules())
        self.assertEqual(len(acl_rules), 6)
        self.assertTrue(all(r.id not in deleted_ids for r in acl_rules))

        acl_rule = AccessControlRule(
            role=ACLRole.READER,
            scope_type=ACLScopeType.GROUP,
            scope_value='group-mail1@gmail.com'
        )
        with self.assertRaises(ValueError):
            # no acl_id
            self.gc.delete_acl_rule(acl_rule)

        with self.assertRaises(TypeError):
            # should be a AccessControlRule or acl rule id as a string
            self.gc.delete_acl_rule(acl_rule=None)
