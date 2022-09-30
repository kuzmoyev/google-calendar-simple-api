Google Calendar Simple API
==========================

.. image:: https://badge.fury.io/py/gcsa.svg
    :target: https://badge.fury.io/py/gcsa
    :alt: PyPi Package

.. image:: https://readthedocs.org/projects/google-calendar-simple-api/badge/?version=latest
    :target: https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/kuzmoyev/Google-Calendar-Simple-API/workflows/Tests/badge.svg
    :target: https://github.com/kuzmoyev/Google-Calendar-Simple-API/actions
    :alt: Tests

.. image:: https://badgen.net/badge/icon/discord?icon=discord&label
    :target: https://discord.gg/mRAegbwYKS
    :alt: Discord


`Google Calendar Simple API` or `gcsa` is a library that simplifies event and calendar management in Google Calendars.
It is a Pythonic object oriented adapter for the official API. See the full `documentation`_.

Installation
------------

.. code-block:: bash

    pip install gcsa

See `Getting started page`_ for more details and installation options.

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
        location='Záhřebská 468/21',
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


**Suggestion**: use beautiful_date_ to create `date` and `datetime` objects in your
projects (*because its beautiful... just like you*).


References
----------

Template for `setup.py` was taken from `kennethreitz/setup.py`_


.. _documentation: https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest
.. _`Getting started page`: https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html
.. _beautiful_date: https://github.com/kuzmoyev/beautiful-date
.. _`kennethreitz/setup.py`: https://github.com/kennethreitz/setup.py
