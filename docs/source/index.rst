Welcome to Google Calendar Simple API documentation!
======================================================

`Google Calendar Simple API` or `gcsa` is a library that simplifies event and calendar management in Google Calendars.
It is a Pythonic object oriented adapter for the `official API`_.

Example usage
-------------

List events
~~~~~~~~~~~

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    calendar = GoogleCalendar('your_email@gmail.com')
    for event in calendar:
        print(event)


Create event
~~~~~~~~~~~~

.. code-block:: python

    from gcsa.event import Event

    event = Event(
        'The Glass Menagerie',
        start=datetime(2020, 7, 10, 19, 0),
        location='Záhřebská 468/21'
        minutes_before_popup_reminder=15
    )
    calendar.add_event(event)


Create recurring event
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gcsa.recurrence import Recurrence, DAILY

    event = Event(
        'Breakfast',
        start=date(2020, 7, 16),
        recurrence=Recurrence.rule(freq=DAILY)
    )
    calendar.add_event(event)


Contents
--------

.. toctree::
   :maxdepth: 2

   getting_started
   authentication
   events
   calendars
   attendees
   attachments
   conference
   reminders
   recurrence
   serializers
   settings
   why_gcsa
   change_log
   code/code

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


References
==========

Template for `setup.py` was taken from `kennethreitz/setup.py`_.


.. _kennethreitz/setup.py: https://github.com/kennethreitz/setup.py
.. _`official API`: https://developers.google.com/calendar