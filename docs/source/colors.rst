.. _colors:

Colors
======

`gcsa` allows you to retrieve a list of available calendar and event colors with their ids.

To do so, create a :py:class:`~gcsa.google_calendar.GoogleCalendar` instance (see :ref:`getting_started` to get your
credentials):

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar

    gc = GoogleCalendar()

.. note::  | Google's API always returns "classic" colors.
           | They are always the same, so you can just use IDs from the tables bellow.
           | You can choose between "classic" and "modern" color sets in the UI. Color names and IDs are the same,
             but the colors are different (see the tables bellow).

Event colors
~~~~~~~~~~~~

List event colors
-----------------

.. code-block:: python

    for color_id, color in gc.list_event_colors().items():
        bg = color['background']
        fg = color['foreground']
        print(color_id, f'{bg=}, {fg=}')

.. CSS classes
.. role:: lavender-classic-e
.. role:: lavender-modern-e
.. role:: sage-classic-e
.. role:: sage-modern-e
.. role:: grape-classic-e
.. role:: grape-modern-e
.. role:: flamingo-classic-e
.. role:: flamingo-modern-e
.. role:: banana-classic-e
.. role:: banana-modern-e
.. role:: tangerine-classic-e
.. role:: tangerine-modern-e
.. role:: peacock-classic-e
.. role:: peacock-modern-e
.. role:: graphite-classic-e
.. role:: graphite-modern-e
.. role:: blueberry-classic-e
.. role:: blueberry-modern-e
.. role:: basil-classic-e
.. role:: basil-modern-e
.. role:: tomato-classic-e
.. role:: tomato-modern-e



.. table:: Event colors
    :widths: 1 1 1 1

    +----------+------------------+-------------------------------------+-------------------------------------+
    | Color ID | Name             | Classic                             |  Modern                             |
    +==========+==================+=====================================+=====================================+
    | '1'      | Lavender         | :lavender-classic-e:`#A4BDFC`       | :lavender-modern-e:`#7986CB`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '2'      | Sage             | :sage-classic-e:`#7AE7BF`           | :sage-modern-e:`#33B679`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '3'      | Grape            | :grape-classic-e:`#DBADFF`          | :grape-modern-e:`#8E24AA`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '4'      | Flamingo         | :flamingo-classic-e:`#FF887C`       | :flamingo-modern-e:`#E67C73`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '5'      | Banana           | :banana-classic-e:`#FBD75B`         | :banana-modern-e:`#F6BF26`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '6'      | Tangerine        | :tangerine-classic-e:`#FFB878`      | :tangerine-modern-e:`#F4511E`       |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '7'      | Peacock          | :peacock-classic-e:`#46D6DB`        | :peacock-modern-e:`#039BE5`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '8'      | Graphite         | :graphite-classic-e:`#E1E1E1`       | :graphite-modern-e:`#616161`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '9'      | Blueberry        | :blueberry-classic-e:`#5484ED`      | :blueberry-modern-e:`#3F51B5`       |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '10'     | Basil            | :basil-classic-e:`#51B749`          | :basil-modern-e:`#0B8043`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '11'     | Tomato           | :tomato-classic-e:`#DC2127`         | :tomato-modern-e:`#D50000`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | None     | Color of the calendar                                                                        |
    +----------+------------------+-------------------------------------+-------------------------------------+


Set event color
---------------

Use color ID in :py:class:`~gcsa.event.Event`'s `color_id` field:

.. code-block:: python

    from gcsa.event import Event

    FLAMINGO_COLOR_ID = '4'
    event = Event('Important!',
                  start=start,
                  color_id=FLAMINGO_COLOR_ID)
    event = gc.add_event(event)


Update event color
------------------

.. code-block:: python

    FLAMINGO_COLOR_ID = '4'
    event.color_id = FLAMINGO_COLOR_ID
    gc.update_event(event)



Calendar colors
~~~~~~~~~~~~~~~

.. note:: Color is a property of a calendar list entry, not a calendar itself (see the difference in :ref:`calendars`).
          Unlike events' colors, you can use either the color ID or hex values to set a color for a calendar list entry.
          If you use hex values (they are not limited to values from the table bellow), value of the color ID will be
          set automatically to the best matching option.

List calendar colors
--------------------

.. code-block:: python

    for color_id, color in gc.list_calendar_colors().items():
        bg = color['background']
        fg = color['foreground']
        print(color_id, f'{bg=}, {fg=}')

.. CSS classes
.. role:: cocoa-classic-c
.. role:: cocoa-modern-c
.. role:: flamingo-classic-c
.. role:: flamingo-modern-c
.. role:: tomato-classic-c
.. role:: tomato-modern-c
.. role:: tangerine-classic-c
.. role:: tangerine-modern-c
.. role:: pumpkin-classic-c
.. role:: pumpkin-modern-c
.. role:: mango-classic-c
.. role:: mango-modern-c
.. role:: eucalyptus-classic-c
.. role:: eucalyptus-modern-c
.. role:: basil-classic-c
.. role:: basil-modern-c
.. role:: pistachio-classic-c
.. role:: pistachio-modern-c
.. role:: avocado-classic-c
.. role:: avocado-modern-c
.. role:: citron-classic-c
.. role:: citron-modern-c
.. role:: banana-classic-c
.. role:: banana-modern-c
.. role:: sage-classic-c
.. role:: sage-modern-c
.. role:: peacock-classic-c
.. role:: peacock-modern-c
.. role:: cobalt-classic-c
.. role:: cobalt-modern-c
.. role:: blueberry-classic-c
.. role:: blueberry-modern-c
.. role:: lavender-classic-c
.. role:: lavender-modern-c
.. role:: wisteria-classic-c
.. role:: wisteria-modern-c
.. role:: graphite-classic-c
.. role:: graphite-modern-c
.. role:: birch-classic-c
.. role:: birch-modern-c
.. role:: radicchio-classic-c
.. role:: radicchio-modern-c
.. role:: cherry-blossom-classic-c
.. role:: cherry-blossom-modern-c
.. role:: grape-classic-c
.. role:: grape-modern-c
.. role:: amethyst-classic-c
.. role:: amethyst-modern-c

.. table:: Calendar colors
    :widths: 1 1 1 1

    +----------+------------------+-------------------------------------+-------------------------------------+
    | Color ID | Name             | Classic                             |  Modern                             |
    +==========+==================+=====================================+=====================================+
    | '1'      | Cocoa            | :cocoa-classic-c:`#AC725E`          | :cocoa-modern-c:`#795548`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '2'      | Flamingo         | :flamingo-classic-c:`#D06B64`       | :flamingo-modern-c:`#E67C73`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '3'      | Tomato           | :tomato-classic-c:`#F83A22`         | :tomato-modern-c:`#D50000`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '4'      | Tangerine        | :tangerine-classic-c:`#FA573C`      | :tangerine-modern-c:`#F4511E`       |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '5'      | Pumpkin          | :pumpkin-classic-c:`#FF7537`        | :pumpkin-modern-c:`#EF6C00`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '6'      | Mango            | :mango-classic-c:`#FFAD46`          | :mango-modern-c:`#F09300`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '7'      | Eucalyptus       | :eucalyptus-classic-c:`#42D692`     | :eucalyptus-modern-c:`#009688`      |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '8'      | Basil            | :basil-classic-c:`#16A765`          | :basil-modern-c:`#0B8043`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '9'      | Pistachio        | :pistachio-classic-c:`#7BD148`      | :pistachio-modern-c:`#7CB342`       |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '10'     | Avocado          | :avocado-classic-c:`#B3DC6C`        | :avocado-modern-c:`#C0CA33`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '11'     | Citron           | :citron-classic-c:`#FBE983`         | :citron-modern-c:`#E4C441`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '12'     | Banana           | :banana-classic-c:`#FAD165`         | :banana-modern-c:`#F6BF26`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '13'     | Sage             | :sage-classic-c:`#92E1C0`           | :sage-modern-c:`#33B679`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '14'     | Peacock          | :peacock-classic-c:`#9FE1E7`        | :peacock-modern-c:`#039BE5`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '15'     | Cobalt           | :cobalt-classic-c:`#9FC6E7`         | :cobalt-modern-c:`#4285F4`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '16'     | Blueberry        | :blueberry-classic-c:`#4986E7`      | :blueberry-modern-c:`#3F51B5`       |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '17'     | Lavender         | :lavender-classic-c:`#9A9CFF`       | :lavender-modern-c:`#7986CB`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '18'     | Wisteria         | :wisteria-classic-c:`#B99AFF`       | :wisteria-modern-c:`#B39DDB`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '19'     | Graphite         | :graphite-classic-c:`#C2C2C2`       | :graphite-modern-c:`#616161`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '20'     | Birch            | :birch-classic-c:`#CABDBF`          | :birch-modern-c:`#A79B8E`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '21'     | Radicchio        | :radicchio-classic-c:`#CCA6AC`      | :radicchio-modern-c:`#AD1457`       |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '22'     | Cherry Blossom   | :cherry-blossom-classic-c:`#F691B2` | :cherry-blossom-modern-c:`#D81B60`  |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '23'     | Grape            | :grape-classic-c:`#CD74E6`          | :grape-modern-c:`#8E24AA`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '24'     | Amethyst         | :amethyst-classic-c:`#A47AE2`       | :amethyst-modern-c:`#9E69AF`        |
    +----------+------------------+-------------------------------------+-------------------------------------+



Set calendar list entry color
-----------------------------

Use color ID in :py:class:`~gcsa.calendar.CalendarListEntry`'s `color_id` field or hex values in `background_color` and
`foreground_color`:

1. Get a calendar list entry

.. code-block:: python

    calendar_list_entry = gc.get_calendar_list_entry('<calendar_id>')

2. Set a new color ID

.. code-block:: python

    GRAPHITE_COLOR_ID = '19'
    calendar_list_entry.color_id = GRAPHITE_COLOR_ID

or set hex values of `background_color` and `foreground_color`:

.. code-block:: python

    calendar_list_entry.background_color = "#626364"
    calendar_list_entry.foreground_color = "#FFFFFF"

3. Update calendar list entry:

.. code-block:: python

    calendar_list_entry = gc.update_calendar_list_entry(calendar_list_entry)



.. Add background color from the text to the table cell
.. raw:: html

   <script>
     document.querySelectorAll('td span').forEach(element => {
        let color = element.classList[0]
        element.parentElement.parentElement.classList.add(color)
    })
   </script>