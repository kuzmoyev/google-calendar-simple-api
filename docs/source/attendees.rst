.. _attendees:

Attendees
=========

If you want to add attendee(s) to your event, just create :py:class:`~gcsa.attendee.Attendee` (s) and pass
as a ``attendees`` parameter (you can also pass just email of attendee and the :py:class:`~gcsa.attendee.Attendee`
will be created for you):

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