.. _events:

Events
======

Event in `gcsa` is represented by the class :py:class:`~gcsa.event.Event`. It stores all the needed information about
the event including its summary, starting and ending dates/times, attachments, reminders, recurrence rules, etc.

`gcsa` allows you to create a new events, retrieve, update, move and delete existing events.

To do so, create a :py:class:`~gcsa.google_calendar.GoogleCalendar` instance (see :ref:`getting_started` to get your
credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()


List events
~~~~~~~~~~~

This code will print out events for one year starting today:

.. code-block:: python

    for event in gc:
        print(event)


Specify range of listed events in two ways:

.. code-block:: python

    gc.get_events(start_date, end_date, order_by='updated')

or

.. code-block:: python

    gc[start_date:end_date:'updated']

``start_date`` and ``end_date`` can be ``date`` or ``datetime`` objects. ``order_by`` can be `'startTime'`
or `'updated'`. If not specified, unspecified stable order is used.


Use ``query`` parameter for free text search through all event fields (except for extended properties):

.. code-block:: python

    gc.get_events(query='Meeting')
    gc.get_events(query='John') # Name of attendee

Use ``single_events`` parameter to expand recurring events into instances and only return single one-off events and
instances of recurring events, but not the underlying recurring events themselves.

.. code-block:: python

    gc.get_events(single_events=True)


Get event by id
~~~~~~~~~~~~~~~

.. code-block:: python

    gc.get_event('<event_id>')


List recurring event instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    gc.get_instances('<recurring_event_id>')

or

.. code-block:: python

    gc.get_instances(recurring_event)

where ``recurring_event`` is :py:class:`~gcsa.event.Event` object with set ``event_id``. You'd probably get it from
the ``get_events`` method.


Create event
~~~~~~~~~~~~

.. code-block:: python

    from beautiful_date import Apr, hours
    from gcsa.event import Event

    start = (22/Apr/2019)[12:00]
    end = start + 2 * hours
    event = Event('Meeting',
                  start=start,
                  end=end)

or to create an **all-day** event, use a `date` object:

.. code-block:: python

    from beautiful_date import Aug, days
    from gcsa.event import Event

    start = 1/Aug/2021
    end = start + 7 * days
    event = Event('Vacation',
                  start=start,
                  end=end)


For ``date``/``datetime`` objects you can use Pythons datetime_ module or as in the
example beautiful_date_ library (*because it's beautiful... just like you*).

Now **add** your event to the calendar:

.. code-block:: python

    gc.add_event(event)

See dedicated pages on how to add :ref:`attendees`, :ref:`attachments`, :ref:`conference`, :ref:`reminders`, and
:ref:`recurrence` to an event.


Update event
~~~~~~~~~~~~

.. code-block:: python

    event.location = 'Prague'
    gc.update_event(event)


Import event
~~~~~~~~~~~~

.. code-block:: python

    gc.import_event(event)

This operation is used to add a private copy of an existing event to a calendar.


Move event to another calendar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    gc.move_event(event, destination_calendar_id='primary')


Delete event
~~~~~~~~~~~~

.. code-block:: python

    gc.delete_event(event)


Event has to have ``event_id`` to be updated, moved, or deleted. Events that you get from
:py:meth:`~gcsa.google_calendar.GoogleCalendar.get_events` method already have their ids.
You can also delete the event by providing its id.

.. code-block:: python

    gc.delete_event('<event_id>')


.. _datetime: https://docs.python.org/3/library/datetime.html
.. _beautiful_date: https://github.com/kuzmoyev/beautiful-date
