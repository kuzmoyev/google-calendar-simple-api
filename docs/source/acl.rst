.. _acl:

Access Control List
===================

Access control rule is represented by the class :py:class:`~gcsa.acl.AccessControlRule`.

`gcsa` allows you to add a new access control rule, retrieve, update and delete existing rules.


To do so, create a :py:class:`~gcsa.google_calendar.GoogleCalendar` instance (see :ref:`getting_started` to get your
credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()


List rules
~~~~~~~~~~

.. code-block:: python

    for rule in gc.get_acl_rules():
        print(rule)


Get rule by id
~~~~~~~~~~~~~~

.. code-block:: python

    rule = gc.get_acl_rule(rule_id='<acl_rule_id>')
    print(rule)


Add access rule
~~~~~~~~~~~~~~~

To add a new ACL rule, create an :py:class:`~gcsa.acl.AccessControlRule` object with specified role
(see more in :py:class:`~gcsa.acl.ACLRole`), scope type (see more in :py:class:`~gcsa.acl.ACLScopeType`), and scope
value.

.. code-block:: python

    from gcsa.acl import AccessControlRule, ACLRole, ACLScopeType

    rule = AccessControlRule(
        role=ACLRole.READER,
        scope_type=ACLScopeType.USER,
        scope_value='friend@gmail.com',
    )

    rule = gc.add_acl_rule(rule)
    print(rule.id)


Update access rule
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    rule = gc.get_acl_rule('<acl_rule_id>')
    rule.role = ACLRole.WRITER
    rule = gc.update_acl_rule(rule)


Delete access rule
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    rule = gc.get_acl_rule('<acl_rule_id>')
    gc.delete_acl_rule(rule)
