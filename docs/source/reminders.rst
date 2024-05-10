.. _reminders:

Reminders
---------

To add reminder(s) to an event you can create :py:class:`~gcsa.reminders.EmailReminder` or
:py:class:`~gcsa.reminders.PopupReminder` and pass them as a ``reminders`` parameter (single reminder
or list of reminders):


.. code-block:: python


    from gcsa.reminders import EmailReminder, PopupReminder

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  reminders=EmailReminder(minutes_before_start=30))

or

.. code-block:: python

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  reminders=[
                        EmailReminder(minutes_before_start=30),
                        EmailReminder(minutes_before_start=60),
                        PopupReminder(minutes_before_start=15)
                  ])


You can also simply add reminders by specifying ``minutes_before_popup_reminder`` and/or
``minutes_before_email_reminder`` parameter of the :py:class:`~gcsa.event.Event` object:

.. code-block:: python

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  minutes_before_popup_reminder=15,
                  minutes_before_email_reminder=30)


If you want to add a reminder to an existing event use :py:meth:`~gcsa.event.Event.add_email_reminder`
and/or :py:meth:`~gcsa.event.Event.add_popup_reminder` methods:


.. code-block:: python

    event.add_popup_reminder(minutes_before_start=30)
    event.add_email_reminder(minutes_before_start=50)

Update event using :py:meth:`~gcsa.google_calendar.GoogleCalendar.update_event` method to save the changes.

To use default reminders of the calendar, set ``default_reminders`` parameter of the :py:class:`~gcsa.event.Event`
to ``True``.

.. note:: You can add up to 5 reminders to one event.

Specific time reminders
~~~~~~~~~~~~~~~~~~~~~~~

You can also set specific time for a reminder.

.. code-block:: python

    from datetime import time

    event = Event(
        'Meeting',
        start=(22/Apr/2019)[12:00],
        reminders=[
            # Day before the event at 13:30
            EmailReminder(days_before=1, at=time(13, 30)),
            # 2 days before the event at 19:15
            PopupReminder(days_before=2, at=time(19, 15))
        ]
    )

    event.add_popup_reminder(days_before=3, at=time(8, 30))
    event.add_email_reminder(days_before=4, at=time(9, 0))


.. note:: Google calendar API only works with ``minutes_before_start``.
    The GCSA's interface that uses ``days_before`` and ``at`` arguments is only a convenient way of setting specific time.
    GCSA will convert ``days_before`` and ``at`` to ``minutes_before_start`` during API requests.
    So after you add or update the event, it will have reminders with only ``minutes_before_start`` set even if they
    were initially created with ``days_before`` and ``at``.

    .. code-block:: python

        from datetime import time

        event = Event(
            'Meeting',
            start=(22/Apr/2019)[12:00],
            reminders=[
                # Day before the event at 12:00
                EmailReminder(days_before=1, at=time(12, 00))
            ]
        )

        event.reminders[0].minutes_before_start is None
        event.reminders[0].days_before == 1
        event.reminders[0].at == time(12, 00)

        event = gc.add_event(event)

        event.reminders[0].minutes_before_start == 24 * 60  # exactly one day before
        event.reminders[0].days_before is None
        event.reminders[0].at is None

    GCSA does not convert ``minutes_before_start`` to ``days_before`` and ``at`` (even for the whole-day events)
    for backwards compatibility reasons.

