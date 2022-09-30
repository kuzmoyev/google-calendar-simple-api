.. _calendars:

Calendars and Calendar list
============================

Calendars in `gcsa` are represented by the :py:class:`~gcsa.calendar.Calendar` and
:py:class:`~gcsa.calendar.CalendarListEntry` classes.


Calendars vs Calendar List
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The **Calendars** collection represents all existing calendars. It can be used to create and delete calendars. You can also
retrieve or set global properties shared across all users with access to a calendar. For example, a calendar's title and
default time zone are global properties.

The **Calendar List** is a collection of all calendar entries that a user has added to their list (shown in the left panel
of the web UI). You can use it to add and remove existing calendars to/from the users’ list. You also use it to retrieve
and set the values of user-specific calendar properties, such as default reminders. Another example is foreground color,
since different users can have different colors set for the same calendar.

The **GoogleCalendar** is a service responsible for processing API requests.

Calendars
~~~~~~~~~

`gcsa` allows you to create a new calendar, retrieve, update, delete and clear existing calendars.

To do so, create a :py:class:`~gcsa.google_calendar.GoogleCalendar` instance (see :ref:`getting_started` to get your
credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()


Get calendar by id
------------------
This returns an objects that stores metadata of the calendar (see more in :py:class:`~gcsa.calendar.Calendar`).

Get a calendar specified as a default in `GoogleCalendar()`

.. code-block:: python

    calendar = gc.get_calendar()

To get a calendar other than the one specified as a default in `GoogleCalendar()`

.. code-block:: python

    calendar = gc.get_calendar('<calendar_id>')


Add a secondary calendar
------------------------

.. code-block:: python

    from gcsa.calendar import Calendar

    calendar = Calendar(
        'Travel calendar',
        description = 'Calendar for travel related events'
    )
    calendar = gc.add_calendar(calendar)


Update calendar
---------------

.. code-block:: python

    calendar.summary = 'New summary'
    calendar.description = 'New description'
    calendar = gc.update_calendar(calendar)


Delete calendar
---------------

.. code-block:: python

    gc.delete_calendar(calendar)

or by id

.. code-block:: python

    gc.delete_calendar('<calendar_id>')


Calendar has to have ``calendar_id`` to be updated or deleted. Calendars that you get from
:py:meth:`~gcsa.google_calendar.GoogleCalendar.get_calendar_list` method already have their ids.
You can also delete the calendar by providing its id.


Clear calendar
--------------

You can only clear (remove all events from) **primary** calendar.

.. code-block:: python

    gc.clear_calendar()

.. warning::
    This will always try to clear a **primary** calendar, regardless of the `default_calendar` value.


Calendar List
~~~~~~~~~~~~~

`gcsa` allows you to add an existing calendar into the user's calendar list, retrieve user's calendar list,
retrieve, update, and delete single entries in the user's calendar list.

To do so, create a :py:class:`~gcsa.google_calendar.GoogleCalendar` instance (see :ref:`getting_started` to get your
credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()


Get user's calendar list
------------------------

This returns the collection of calendars in the user's calendar list.
(see more in :py:class:`~gcsa.calendar.CalendarListEntry`).

.. code-block:: python

    calendars = gc.get_calendar_list()

you can include deleted and hidden entries and specify the minimal access role:

.. code-block:: python

    from gcsa.calendar import AccessRoles

    calendars = gc.get_calendar_list(
        min_access_role=AccessRoles.READER
        show_deleted=True,
        show_hidden=True
    )

Get calendar list entry by id
-----------------------------

Get a calendar specified as a default in `GoogleCalendar()`

.. code-block:: python

    gc.get_calendar_list_entry()


To get calendar other then the one specified as a default in `GoogleCalendar()`


.. code-block:: python

    gc.get_calendar_list_entry('calendar_id')


Add calendar list entry
-----------------------

This adds an existing calendar into the user's calendar list
(see more in :py:class:`~gcsa.calendar.CalendarListEntry`):


.. code-block:: python

    from gcsa.calendar import CalendarListEntry

    calendar_list_entry = CalendarListEntry(
        calendar_id='calendar_id',
        summary_override='Holidays in Czechia'
    )
    gc.add_calendar_list_entry(calendar_list_entry)

You can make a :py:class:`~gcsa.calendar.CalendarListEntry` out of :py:class:`~gcsa.calendar.Calendar` with
:py:meth:`~gcsa.calendar.Calendar.to_calendar_list_entry` method:


.. code-block:: python

    calendar = Calendar(
        calendar_id='calendar_id',
        summary='Státní svátky v ČR'
    )
    calendar_list_entry = calendar.to_calendar_list_entry(
        summary_override='Holidays in Czechia'
    )
    gc.add_calendar_list_entry(calendar_list_entry)


Update calendar list entry
--------------------------

.. code-block:: python

    calendar_list_entry.summary_override = 'Holidays in Czechia 2022'
    gc.update_calendar_list_entry(calendar_list_entry)

Delete calendar list entry
--------------------------

You can use :py:class:`~gcsa.calendar.CalendarListEntry`, :py:class:`~gcsa.calendar.Calendar`, or calendar id:

.. code-block:: python

    gc.delete_calendar_list_entry(calendar)

or

.. code-block:: python

    gc.delete_calendar_list_entry(calendar_list_entry)

or

.. code-block:: python

    gc.delete_calendar_list_entry('<calendar_id>')

