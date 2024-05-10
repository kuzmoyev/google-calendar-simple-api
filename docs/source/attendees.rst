.. _attendees:

Attendees
=========

If you want to add attendee(s) to your event, just create :py:class:`~gcsa.attendee.Attendee` (s) and pass
as an ``attendees`` parameter (you can also pass just an email of the attendee and
the :py:class:`~gcsa.attendee.Attendee` will be created for you):

.. code-block:: python

    from gcsa.attendee import Attendee

    attendee = Attendee(
        'attendee@gmail.com',
        display_name='Friend',
        additional_guests=3
    )

    event = Event('Meeting',
                  start=(17/Jul/2020)[12:00],
                  attendees=attendee)

or

.. code-block:: python

    event = Event('Meeting',
                  start=(17/Jul/2020)[12:00],
                  attendees='attendee@gmail.com')

You can pass multiple attendees at once in a list.


.. code-block:: python

    event = Event('Meeting',
                  start=(17/Jul/2020)[12:00],
                  attendees=[
                      'attendee@gmail.com',
                      Attendee('attendee2@gmail.com', display_name='Friend')
                  ])

To **notify** attendees about created/updated/deleted event use `send_updates` parameter in `add_event`, `update_event`,
and `delete_event` methods. See :py:class:`~gcsa.google_calendar.SendUpdatesMode` for possible values.

To add attendees to an existing event use its :py:meth:`~gcsa.event.Event.add_attendee` method:

.. code-block:: python

    event.add_attendee(
            Attendee('attendee@gmail.com',
                display_name='Friend',
                additional_guests=3
            )
    )

or

.. code-block:: python

    event.add_attendee('attendee@gmail.com')

to add a single attendee.

Use :py:meth:`~gcsa.event.Event.add_attendees` method to add multiple at once:

.. code-block:: python

    event.add_attendees(
        [
            Attendee('attendee@gmail.com',
                display_name='Friend',
                additional_guests=3
            ),
            'attendee_by_email1@gmail.com',
            'attendee_by_email2@gmail.com'
        ]
    )

Update event using :py:meth:`~gcsa.google_calendar.GoogleCalendar.update_event` method to save the changes.
