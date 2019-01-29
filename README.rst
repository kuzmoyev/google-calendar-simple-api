Google Calendar Simple API
==========================

.. image:: https://travis-ci.com/kuzmoyev/Google-Calendar-Simple-API.svg?branch=master
    :target: https://travis-ci.com/kuzmoyev/Google-Calendar-Simple-API

.. image:: https://readthedocs.org/projects/google-calendar-simple-api/badge/?version=latest
    :target: https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


`Google Calendar Simple API` or `gcsa` is a library that simplifies event management in a Google Calendars.
It is a Pythonic object oriented adapter for the `official API`_.

Installation
------------

::

    pip install gcsa

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


See documentation_
for more parameters and functionality.

**Suggestion**: use beautiful_date_ to creat `date` and `datetime` objects in your
projects (*because its beautiful... just like you*).


References
----------

Template for `setup.py` was taken from `kennethreitz/setup.py`_


.. _`official API`: https://github.com/googleapis/google-api-python-client
.. _documentation: https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest
.. _beautiful_date: https://github.com/beautiful-everything/beautiful-date
.. _`kennethreitz/setup.py`: https://github.com/kennethreitz/setup.py