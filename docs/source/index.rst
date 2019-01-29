Welcome to Google Calendar Simple API's documentation!
======================================================

`Google Calendar Simple API` or `gcsa` is a library that simplifies event management in a Google Calendars.
It is a Pythonic object oriented adapter for the `official API`_.

Example usage
-------------

::

    calendar = GoogleCalendar('your_email@gmail.com')
    event = Event(
        'Breakfast',
        start=date(2019, 1, 1),
        recurrence=Recurrence.rule(freq=DAILY)),
        minutes_before_email_reminder=50
    )

    calendar.add_event(event)

    for event in calendar:
        print(event)


Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   code
   event_management

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


References
==========

Template for `setup.py` was taken from `kennethreitz/setup.py`_.


.. _kennethreitz/setup.py: https://github.com/kennethreitz/setup.py
.. _`official API`: https://github.com/googleapis/google-api-python-client