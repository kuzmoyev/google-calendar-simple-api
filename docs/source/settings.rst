.. _settings:

Settings
========

You can retrieve user's settings for the given account with :py:meth:`~gcsa.google_calendar.GoogleCalendar.get_settings`.

To do so, create a :py:class:`~gcsa.google_calendar.GoogleCalendar` instance (see :ref:`getting_started` to get your
credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()


Following code will return a corresponding :py:class:`~gcsa.settings.Settings` object:

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()
    settings = gc.get_settings()
    print(settings)

.. code-block:: python

        User settings:
        auto_add_hangouts=true
        date_field_order=DMY
        default_event_length=60
        format24_hour_time=false
        hide_invitations=false
        hide_weekends=false
        locale=en
        remind_on_responded_events_only=false
        show_declined_events=true
        timezone=Europe/Prague
        use_keyboard_shortcuts=true
        week_start=1

