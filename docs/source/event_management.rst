Event management
================

Event in `gcsa` is represented by the class :py:class:`~gcsa.event.Event`. It stores all needed information about event
including its summary, starting and ending dates/times, attachments, reminders, recurrence rules, etc.

Current version of `gcsa` allows you to create new events, delete existing events and list existing events.

To do so, create a ``GoogleCalendar`` instance (see :ref:`installation` to get your credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    calendar = GoogleCalendar()

then you can **list** existing events.

This code will print out events for one year starting today:


.. code-block:: python

    for event in calendar:
        print(event)


You can specify range of listed events in two ways:

.. code-block:: python

    calendar.get_event(start_date, end_date, order_by='updated')

or

.. code-block:: python

    calendar[start_date:end_date:'updated']

``start_date`` and ``end_date`` can be ``date`` or ``datetime`` objects. ``order_by`` can be `'startTime'` (default)
or `'updated'`.



You can **create** an event:

.. code-block:: python

    from beautiful_date import Apr

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  end=(22/Apr/2019)[13:00])


For ``date``/``datetime`` objects you can use Pythons datetime_ module or as in the
example beautiful_date_ library (*because it's beautiful... just like you*).


Now you can **add** your event to the calendar:

.. code-block:: python

    calendar.add_event(event)


To **delete** an event:


.. code-block:: python

    calendar.delete_event(event)



Event has to have ``event_id`` to be deleted. Events that you get from
:py:meth:`~gcsa.google_calendar.GoogleCalendar.get_events` method already have their ids.

Attachments
-----------

If you want to add and attachment(s) to your event, just create :py:class:`~gcsa.attachment.Attachment` (s) and pass
as a ``attachments`` parameter:

.. code-block:: python

    from gcsa.attachment import Attachment

    attachment = Attachment('My file',
                            file_url='https://docs.google.com/document/d/1uDvwcxOsXkzl2Bod0YIfrIQ5MqfBhnc1jusYdH1xCZo/edit'
                            mime_type="application/vnd.google-apps.document")

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  attachments=attachment)


You can pass multiple attachments at once in a list.

.. code-block:: python

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  attachments=[attachment1, attachment1])



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
and/or :py:meth:`~gcsa.event.Event.add_popup_reminder` methods.

To use default reminders of the calendar, set ``default_reminders`` parameter of the :py:class:`~gcsa.event.Event`
to ``True``.

.. note:: You can add up to 5 reminders to one event.



.. _datetime: https://docs.python.org/3/library/datetime.html
.. _beautiful_date: https://github.com/beautiful-everything/beautiful-date
