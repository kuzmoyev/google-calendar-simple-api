from gcsa.acl import AccessControlRule
from gcsa.serializers.base_serializer import BaseSerializer


class ACLRuleSerializer(BaseSerializer):
    type_ = AccessControlRule

    def __init__(self, access_control_rule):
        super().__init__(access_control_rule)

    @staticmethod
    def _to_json(acl_rule: AccessControlRule):
        data = {
            "id": acl_rule.id,
            "scope": {
                "type": acl_rule.scope_type,
                "value": acl_rule.scope_value
            },
            "role": acl_rule.role
        }
        data = ACLRuleSerializer._remove_empty_values(data)
        return data

    @staticmethod
    def _to_object(json_acl_rule):
        scope = json_acl_rule.get('scope', {})
        return AccessControlRule(
            acl_id=json_acl_rule.get('id'),
            scope_type=scope.get('type'),
            scope_value=scope.get('value'),
            role=json_acl_rule.get('role')
        )
