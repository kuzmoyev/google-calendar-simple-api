Serializers
===========

The library implements the JSON serializers for all available Google Calendar objects. JSON format is as specified in
the `official API documentation`_. In general, you won't need to use them, ``gcsa`` serializes everything as needed
under the hood. It is documented just so you know they exist and can be used if necessary.

.. note::
    Note that serializers' ``to_json`` methods ignore read-only fields of the objects.
    Read-only fields of the objects are ones that are passed to the parameters of their ``__init__`` with
    underscores, e.g. ``Event(_updated=25/Nov/2020)``.

Events serializer
~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.event import Event
    from gcsa.serializers.event_serializer import EventSerializer


    event = Event(
        'Meeting',
        start=(22 / Nov / 2020)[18:00]
    )

    EventSerializer.to_json(event)

.. code-block:: javascript

    {
        'summary': 'Meeting',
        'start': {
            'dateTime': '2020-11-22T18:00:00+01:00',
            'timeZone': 'Europe/Prague'
        },
        'end': {
            'dateTime': '2020-11-22T19:00:00+01:00',
            'timeZone': 'Europe/Prague'
        },
        'attachments': [],
        'attendees': [],
        'recurrence': [],
        'reminders': {'useDefault': False},
        'visibility': 'default'
    }


To object
---------

.. code-block:: python

    event_json = {
        'start': {
            'dateTime': '2020-11-22T18:00:00+01:00',
            'timeZone': 'Europe/Prague'
        },
        'end': {
            'dateTime': '2020-11-22T19:00:00+01:00',
            'timeZone': 'Europe/Prague'
        },
        'attachments': [],
        'attendees': [],
        'recurrence': [],
        'reminders': {'useDefault': False},
        'summary': 'Meeting',
        'visibility': 'default'
    }

    EventSerializer.to_object(event_json)

.. code-block:: python

    <Event 2020-11-22 18:00:00+01:00 - Meeting>

Attachments serializer
~~~~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.attachment import Attachment
    from gcsa.serializers.attachment_serializer import AttachmentSerializer

    attachment = Attachment(
        file_url='https://bit.ly/3lZo0Cc',
        title='My file',
        mime_type='application/vnd.google-apps.document'
    )

    AttachmentSerializer.to_json(attachment)

.. code-block:: javascript

    {
        'title': 'My file',
        'fileUrl': 'https://bit.ly/3lZo0Cc',
        'mimeType': 'application/vnd.google-apps.document'
    }


To object
---------

.. code-block:: python

    attachment_json = {
        'fileUrl': 'https://bit.ly/3lZo0Cc',
        'mimeType': 'application/vnd.google-apps.document',
        'title': 'My file'
    }

    AttachmentSerializer.to_object(attachment_json)

.. code-block:: python

    <Attachment 'My file' - 'https://bit.ly/3lZo0Cc'>



Person serializer
~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.person import Person
    from gcsa.serializers.person_serializer import PersonSerializer

    person = Person(
        'john@gmail.com',
        display_name='BFF',
    )

    PersonSerializer.to_json(person)

.. code-block:: javascript

    {
        'email': 'john@gmail.com'
        'displayName': 'BFF',
    }


To object
---------


.. code-block:: python

    person_json = {
        'email': 'john@gmail.com',
        'displayName': 'BFF',
        'id': '123123',
        'self': True
    }

    PersonSerializer.to_object(person_json)

.. code-block:: python

    <Person 'john@gmail.com' - 'BFF'>


Attendees serializer
~~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.attendee import Attendee
    from gcsa.serializers.attendee_serializer import AttendeeSerializer

    attendee = Attendee(
        'john@gmail.com',
        display_name='BFF',
        additional_guests=2
    )

    AttendeeSerializer.to_json(attendee)

.. code-block:: javascript

    {
        'email': 'john@gmail.com'
        'displayName': 'BFF',
        'additionalGuests': 2,
    }


To object
---------

.. code-block:: python

    attendee_json = {
        'email': 'john@gmail.com',
        'displayName': 'BFF',
        'additionalGuests': 2,
        'responseStatus': 'needsAction'
    }

    AttendeeSerializer.to_object(attendee_json)

.. code-block:: python

    <Attendee 'john@gmail.com' - response: 'needsAction'>


Conference serializer
~~~~~~~~~~~~~~~~~~~~~

EntryPoint
----------

To json
*******


.. code-block:: python

    from gcsa.conference import EntryPoint
    from gcsa.serializers.conference_serializer import EntryPointSerializer

    entry_point = EntryPoint(
        EntryPoint.VIDEO,
        uri='https://meet.google.com/aaa-bbbb-ccc'
    )

    EntryPointSerializer.to_json(entry_point)

.. code-block:: javascript

    {
        'entryPointType': 'video',
        'uri': 'https://meet.google.com/aaa-bbbb-ccc'
    }


To object
*********

.. code-block:: python

    entry_point_json = {
        'entryPointType': 'video',
        'uri': 'https://meet.google.com/aaa-bbbb-ccc'
    }

    EntryPointSerializer.to_object(entry_point_json)

.. code-block:: python

    <EntryPoint video - 'https://meet.google.com/aaa-bbbb-ccc'>


ConferenceSolution
------------------

To json
*******


.. code-block:: python

    from gcsa.conference import ConferenceSolution, EntryPoint, SolutionType
    from gcsa.serializers.conference_serializer import ConferenceSolutionSerializer

    conference_solution = ConferenceSolution(
        entry_points=EntryPoint(
            EntryPoint.VIDEO,
            uri='https://meet.google.com/aaa-bbbb-ccc'
        ),
        solution_type=SolutionType.HANGOUTS_MEET,
    )

    ConferenceSolutionSerializer.to_json(conference_solution)

.. code-block:: javascript

    {
        'conferenceSolution': {
            'key': {
                'type': 'hangoutsMeet'
            }
        },
        'entryPoints': [
            {
                'entryPointType': 'video',
                'uri': 'https://meet.google.com/aaa-bbbb-ccc'
            }
        ]
    }


To object
*********

.. code-block:: python

    conference_solution_json = {
        'conferenceSolution': {
            'key': {
                'type': 'hangoutsMeet'
            }
        },
        'entryPoints': [
            {
                'entryPointType': 'video',
                'uri': 'https://meet.google.com/aaa-bbbb-ccc'
            }
        ]
    }

    ConferenceSolutionSerializer.to_object(conference_solution_json)

.. code-block:: python

    <ConferenceSolution hangoutsMeet - [<EntryPoint video - 'https://meet.google.com/aaa-bbbb-ccc'>]>


ConferenceSolutionCreateRequest
-------------------------------

To json
*******


.. code-block:: python

    from gcsa.conference import ConferenceSolutionCreateRequest, SolutionType
    from gcsa.serializers.conference_serializer import ConferenceSolutionCreateRequestSerializer

    conference_solution_create_request = ConferenceSolutionCreateRequest(
        solution_type=SolutionType.HANGOUTS_MEET,
    )

    ConferenceSolutionCreateRequestSerializer.to_json(conference_solution_create_request)

.. code-block:: javascript

    {
        'createRequest': {
            'conferenceSolutionKey': {
                'type': 'hangoutsMeet'
            },
            'requestId': '30b8e7c4d595445aa73c3feccf4b4f06'
        }
    }


To object
*********

.. code-block:: python

    conference_solution_create_request_json = {
        'createRequest': {
            'conferenceSolutionKey': {
                'type': 'hangoutsMeet'
            },
            'requestId': '30b8e7c4d595445aa73c3feccf4b4f06',
            'status': {
                'statusCode': 'pending'
            }
        }
    }

    ConferenceSolutionCreateRequestSerializer.to_object(conference_solution_create_request_json)

.. code-block:: python

    <ConferenceSolutionCreateRequest hangoutsMeet - status:'pending'>


Reminders serializer
~~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.reminders import EmailReminder, PopupReminder
    from gcsa.serializers.reminder_serializer import ReminderSerializer

    reminder = EmailReminder(minutes_before_start=30)

    ReminderSerializer.to_json(reminder)

.. code-block:: javascript

    {
        'method': 'email',
        'minutes': 30
    }

.. code-block:: python

    reminder = PopupReminder(minutes_before_start=30)

    ReminderSerializer.to_json(reminder)

.. code-block:: javascript

    {
        'method': 'popup',
        'minutes': 30
    }


To object
---------

.. code-block:: python

    reminder_json = {
        'method': 'email',
        'minutes': 30
    }

    ReminderSerializer.to_object(reminder_json)

.. code-block:: python

    <EmailReminder - minutes_before_start:30>

.. code-block:: python

    reminder_json = {
        'method': 'popup',
        'minutes': 30
    }

    ReminderSerializer.to_object(reminder_json)

.. code-block:: python

    <PopupReminder - minutes_before_start:30>



Calendars serializer
~~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.calendar import Calendar, AccessRoles
    from gcsa.serializers.calendar_serializer import CalendarSerializer

    calendar = Calendar(
        summary='Primary',
        calendar_id='primary',
        description='Description',
        location='Location',
        timezone='Timezone',
        allowed_conference_solution_types=[
            AccessRoles.FREE_BUSY_READER,
            AccessRoles.READER,
            AccessRoles.WRITER,
            AccessRoles.OWNER,
        ]
    )

    CalendarSerializer.to_json(calendar)

.. code-block:: javascript

    {
        'id': 'primary',
        'summary': 'Primary',
        'description': 'Description',
        'location': 'Location',
        'timeZone': 'Timezone',
        'conferenceProperties': {
            'allowedConferenceSolutionTypes': [
                'freeBusyReader',
                'reader',
                'writer',
                'owner'
            ]
        }
    }


To object
---------

.. code-block:: python

    calendar_json = {
        'id': 'primary',
        'summary': 'Primary',
        'description': 'Description',
        'location': 'Location',
        'timeZone': 'Timezone',
        'conferenceProperties': {
            'allowedConferenceSolutionTypes': [
                'freeBusyReader',
                'reader',
                'writer',
                'owner'
            ]
        }
    }
    CalendarSerializer.to_object(calendar_json)

.. code-block:: python

    <Calendar Primary - Description>



CalendarListEntry serializer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.calendar import CalendarListEntry, NotificationType
    from gcsa.reminders import EmailReminder
    from gcsa.serializers.calendar_serializer import CalendarListEntrySerializer

    calendar_list_entry = CalendarListEntry(
        calendar_id='<calendar_id>',
        summary_override='Holidays in Czechia 2022',
        color_id='2',
        background_color='#123456',
        foreground_color='#234567',
        hidden=True,
        selected=False,
        default_reminders=[EmailReminder(minutes_before_start=15)],
        notification_types=[
            NotificationType.EVENT_CREATION,
            NotificationType.EVENT_CHANGE
        ]
    )

    CalendarListEntrySerializer.to_json(calendar_list_entry)

.. code-block:: javascript

    {
        'id': '<calendar_id>',
        'summaryOverride': 'Holidays in Czechia 2022',
        'colorId': '2',
        'backgroundColor': '#123456',
        'foregroundColor': '#234567',
        'hidden': True,
        'selected': False,
        'defaultReminders': [
            {'method': 'email', 'minutes': 15}
        ],
        'notificationSettings': {
            'notifications': [
                {'type': 'eventCreation', 'method': 'email'},
                {'type': 'eventChange', 'method': 'email'}
            ]
        }
    }


To object
---------

.. code-block:: python

    calendar_list_entry_json = {
        'id': '<calendar_id>',
        'summary': 'Státní svátky v ČR',
        'summaryOverride': 'Holidays in Czechia 2022',
        'colorId': '2',
        'backgroundColor': '#123456',
        'foregroundColor': '#234567',
        'hidden': True,
        'selected': False,
        'defaultReminders': [
            {'method': 'email', 'minutes': 15}
        ],
        'notificationSettings': {
            'notifications': [
                {'type': 'eventCreation', 'method': 'email'},
                {'type': 'eventChange', 'method': 'email'}
            ]
        }
    }

    CalendarListEntrySerializer.to_object(calendar_list_entry_json)


.. code-block:: python

    <CalendarListEntry Holidays in Czechia 2022 - (Státní svátky v ČR)>



Access control rule serializer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.acl import AccessControlRule, ACLRole, ACLScopeType
    from gcsa.serializers.acl_rule_serializer import ACLRuleSerializer

    rule = AccessControlRule(
        role=ACLRole.READER,
        scope_type=ACLScopeType.USER,
        scope_value='friend@gmail.com',
    )

    ACLRuleSerializer.to_json(rule)


.. code-block:: javascript

    {
        'role': 'reader',
        'scope': {
            'type': 'user',
            'value': 'friend@gmail.com'
        }
    }


To object
---------

.. code-block:: python

    acl_rule_json = {
        'role': 'reader',
        'scope': {
            'type': 'user',
            'value': 'friend@gmail.com'
        },
        'id': 'user:friend@gmail.com'
    }

    ACLRuleSerializer.to_object(acl_rule_json)

.. code-block:: python

    <AccessControlRule friend@gmail.com - reader>



FreeBusy serializer
~~~~~~~~~~~~~~~~~~~

To json
-------

.. code-block:: python

    from gcsa.free_busy import FreeBusy, TimeRange
    from gcsa.serializers.free_busy_serializer import FreeBusySerializer

    free_busy = FreeBusy(
        time_min=(24 / Mar / 2023)[13:22],
        time_max=(25 / Mar / 2023)[13:22],
        groups={'group1': ['calendar1', 'calendar2']},
        calendars={
            'calendar1': [
                TimeRange((24 / Mar / 2023)[14:22], (24 / Mar / 2023)[15:22]),
                TimeRange((24 / Mar / 2023)[17:22], (24 / Mar / 2023)[18:22]),
            ],
            'calendar2': [
                TimeRange((24 / Mar / 2023)[15:22], (24 / Mar / 2023)[16:22]),
                TimeRange((24 / Mar / 2023)[18:22], (24 / Mar / 2023)[19:22]),
            ]
        },
        groups_errors={
            "non-existing-group": [
                {
                    "domain": "global",
                    "reason": "notFound"
                }
            ]
        },
        calendars_errors={
            "non-existing-calendar": [
                {
                    "domain": "global",
                    "reason": "notFound"
                }
            ]
        }
    )

    FreeBusySerializer.to_json(free_busy)


.. code-block:: javascript

    {
        'calendars': {
            'calendar1': {
                'busy': [
                    {'start': '2023-03-24T14:22:00', 'end': '2023-03-24T15:22:00'},
                    {'start': '2023-03-24T17:22:00', 'end': '2023-03-24T18:22:00'}
                ],
                'errors': []
            },
            'calendar2': {
                'busy': [
                    {'start': '2023-03-24T15:22:00', 'end': '2023-03-24T16:22:00'},
                    {'start': '2023-03-24T18:22:00', 'end': '2023-03-24T19:22:00'}
                ],
                'errors': []
            },
            'non-existing-calendar': {
                'busy': [],
                'errors': [
                    {'domain': 'global', 'reason': 'notFound'}
                ]
            }
        },
        'groups': {
            'group1': {
                'calendars': ['calendar1', 'calendar2'],
                'errors': []
            },
            'non-existing-group': {
                'calendars': [],
                'errors': [
                    {'domain': 'global', 'reason': 'notFound'}
                ]
            }
        },
        'timeMin': '2023-03-24T13:22:00',
        'timeMax': '2023-03-25T13:22:00'
    }


To object
---------

.. code-block:: python

    free_busy_json = {
        'calendars': {
            'calendar1': {
                'busy': [
                    {'start': '2023-03-24T14:22:00', 'end': '2023-03-24T15:22:00'},
                    {'start': '2023-03-24T17:22:00', 'end': '2023-03-24T18:22:00'}
                ],
                'errors': []
            },
            'calendar2': {
                'busy': [
                    {'start': '2023-03-24T15:22:00', 'end': '2023-03-24T16:22:00'},
                    {'start': '2023-03-24T18:22:00', 'end': '2023-03-24T19:22:00'}
                ],
                'errors': []
            },
            'non-existing-calendar': {
                'busy': [],
                'errors': [
                    {'domain': 'global', 'reason': 'notFound'}
                ]
            }
        },
        'groups': {
            'group1': {
                'calendars': ['calendar1', 'calendar2'],
                'errors': []
            },
            'non-existing-group': {
                'calendars': [],
                'errors': [
                    {'domain': 'global', 'reason': 'notFound'}
                ]
            }
        },
        'timeMin': '2023-03-24T13:22:00',
        'timeMax': '2023-03-25T13:22:00'
    }

    FreeBusySerializer.to_object(free_busy_json)

.. code-block:: python

    <FreeBusy 2023-03-24 13:22:00 - 2023-03-25 13:22:00>



.. _`official API documentation`: https://developers.google.com/calendar
