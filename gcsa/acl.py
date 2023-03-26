from gcsa._resource import Resource


class ACLRole:
    """
    * `NONE` - Provides no access.
    * `FREE_BUSY_READER` - Provides read access to free/busy information.
    * `READER` - Provides read access to the calendar. Private events will appear to users with reader access, but event
                 details will be hidden.
    * `WRITER` - Provides read and write access to the calendar. Private events will appear to users with writer access,
                 and event details will be visible.
    * `OWNER` - Provides ownership of the calendar. This role has all of the permissions of the writer role with
                the additional ability to see and manipulate ACLs.
    """

    NONE = "none"
    FREE_BUSY_READER = "freeBusyReader"
    READER = "reader"
    WRITER = "writer"
    OWNER = "owner"


class ACLScopeType:
    """
    * `DEFAULT` - The public scope.
    * `USER` - Limits the scope to a single user.
    * `GROUP` - Limits the scope to a group.
    * `DOMAIN` - Limits the scope to a domain.
    """

    DEFAULT = "default"
    USER = "user"
    GROUP = "group"
    DOMAIN = "domain"


class AccessControlRule(Resource):
    def __init__(
            self,
            *,
            role: str,
            scope_type: str,
            acl_id: str = None,
            scope_value: str = None
    ):
        """
        :param role:
                The role assigned to the scope. See :py:class:`~gcsa.acl.ACLRole`.
        :param scope_type:
                The type of the scope. See :py:class:`~gcsa.acl.ACLScopeType`.
        :param acl_id:
                Identifier of the Access Control List (ACL) rule.
        :param scope_value:
                The email address of a user or group, or the name of a domain, depending on the scope type.
                Omitted for type "default".
        """
        self.acl_id = acl_id
        self.role = role
        self.scope_type = scope_type
        self.scope_value = scope_value

    @property
    def id(self):
        return self.acl_id

    def __str__(self):
        return '{} - {}'.format(self.scope_value, self.role)

    def __repr__(self):
        return '<AccessControlRule {}>'.format(self.__str__())
