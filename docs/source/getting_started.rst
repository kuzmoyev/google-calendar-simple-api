.. _getting_started:

Getting started
===============


Installation
------------

To install ``gcsa`` run the following command:

.. code-block:: bash

   pip install gcsa


from sources:

.. code-block:: bash

    git clone git@github.com:kuzmoyev/google-calendar-simple-api.git
    cd google-calendar-simple-api
    python setup.py install

Credentials
-----------

Now you need to get your API credentials:

    1. Go to `Calendar API Quickstart`_
    2. Click ``ENABLE THE GOOGLE CALENDAR API``
    3. Click ``DOWNLOAD CLIENT CONFIGURATION``
    4. Put downloaded ``credentials.json`` file into ``~/.credentials/`` directory

See more options in :ref:`authentication`.

    .. note:: You can put ``credentials.json`` file anywhere you want and specify
        the path to it in your code afterwords. But remember not to share it (e.g. add it
        to ``.gitignore``) as it is your private credentials.

    .. note::
        | On the first run, your application will prompt you to the default browser
          to get permissions from you to use your calendar. This will create
          ``token.pickle`` file in the same folder (unless specified otherwise) as your
          ``credentials.json``. So don't forget to also add it to ``.gitignore`` if
          it is in a GIT repository.
        | If you don't want to save it in ``.pickle`` file, you can use ``save_token=False``
          when initializing the ``GoogleCalendar``.

Quick example
-------------

The following code will create a recurrent event in your calendar starting on January 1 and
repeating everyday at 9:00am except weekends and two holidays (April 19, April 22).

Then it will list all events for one year starting today.

For ``date``/``datetime`` objects you can use Pythons datetime_ module or as in the
example beautiful_date_ library (*because it's beautiful... just like you*).

.. code-block:: python

    from gcsa.event import Event
    from gcsa.google_calendar import GoogleCalendar
    from gcsa.recurrence import Recurrence, DAILY, SU, SA

    from beautiful_date import Jan, Apr


    calendar = GoogleCalendar('your_email@gmail.com')
    event = Event(
        'Breakfast',
        start=(1 / Jan / 2019)[9:00],
        recurrence=[
            Recurrence.rule(freq=DAILY),
            Recurrence.exclude_rule(by_week_day=[SU, SA]),
            Recurrence.exclude_times([
                (19 / Apr / 2019)[9:00],
                (22 / Apr / 2019)[9:00]
            ])
        ],
        minutes_before_email_reminder=50
    )

    calendar.add_event(event)

    for event in calendar:
        print(event)

.. _`Calendar API Quickstart`: https://developers.google.com/calendar/quickstart/python#step_1_turn_on_the
.. _datetime: https://docs.python.org/3/library/datetime.html
.. _beautiful_date: https://github.com/kuzmoyev/beautiful-date
