Google Calendar Simple API
==========================


.. image:: https://github.com/kuzmoyev/Google-Calendar-Simple-API/workflows/Tests/badge.svg
    :target: https://github.com/kuzmoyev/Google-Calendar-Simple-API/actions
    :alt: Tests

.. image:: https://readthedocs.org/projects/google-calendar-simple-api/badge/?version=latest
    :target: https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: https://pepy.tech/badge/gcsa
    :target: https://pepy.tech/project/gcsa
    :alt: Downloads

.. image:: https://badge.fury.io/py/gcsa.svg
    :target: https://badge.fury.io/py/gcsa
    :alt: Downloads



`Google Calendar Simple API` or `gcsa` is a library that simplifies event management in a Google Calendars.
It is a Pythonic object oriented adapter for the `official API`_.

Installation
------------

::

    pip install gcsa

Example usage
-------------

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar
    from gcsa.event import Event
    from gcsa.recurrence import Recurrence, DAILY

    calendar = GoogleCalendar('your_email@gmail.com')
    event = Event(
        'Breakfast',
        start=date(2020, 6, 14),
        recurrence=Recurrence.rule(freq=DAILY),
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