Serializers
===========

The library implements the JSON serializers for all available Google Calendar objects. JSON format is as specified in
the `official API documentation`_. In general, you won't need to use them, ``gcsa`` serializes everything as needed
under the hood. It is documented just so you know they exist and can be used if necessary.

.. note::
    Note that serializer's ``to_json`` methods ignore read-only fields of the objects.
    Read only fields of the objects are ones that are passed to the parameters of their ``__init__`` with
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




.. _`official API documentation`: https://developers.google.com/calendar
