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
