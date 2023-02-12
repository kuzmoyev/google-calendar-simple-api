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
.. role:: lavender-classic
.. role:: lavender-modern
.. role:: sage-classic
.. role:: sage-modern
.. role:: grape-classic
.. role:: grape-modern
.. role:: flamingo-classic
.. role:: flamingo-modern
.. role:: banana-classic
.. role:: banana-modern
.. role:: tangerine-classic
.. role:: tangerine-modern
.. role:: peacock-classic
.. role:: peacock-modern
.. role:: graphite-classic
.. role:: graphite-modern
.. role:: blueberry-classic
.. role:: blueberry-modern
.. role:: basil-classic
.. role:: basil-modern
.. role:: tomato-classic
.. role:: tomato-modern



.. table:: Calendar colors
    :widths: 1 1 1 1

    +----------+------------------+-------------------------------------+-------------------------------------+
    | Color ID | Name             | Classic                             |  Modern                             |
    +==========+==================+=====================================+=====================================+
    | '1'      | Lavender         | :lavender-classic:`#A4BDFC`         | :lavender-modern:`#7986CB`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '2'      | Sage             | :sage-classic:`#7AE7BF`             | :sage-modern:`#33B679`              |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '3'      | Grape            | :grape-classic:`#DBADFF`            | :grape-modern:`#8E24AA`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '4'      | Flamingo         | :flamingo-classic:`#FF887C`         | :flamingo-modern:`#E67C73`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '5'      | Banana           | :banana-classic:`#FBD75B`           | :banana-modern:`#F6BF26`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '6'      | Tangerine        | :tangerine-classic:`#FFB878`        | :tangerine-modern:`#F4511E`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '7'      | Peacock          | :peacock-classic:`#46D6DB`          | :peacock-modern:`#039BE5`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '8'      | Graphite         | :graphite-classic:`#E1E1E1`         | :graphite-modern:`#616161`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '9'      | Blueberry        | :blueberry-classic:`#5484ED`        | :blueberry-modern:`#3F51B5`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '10'     | Basil            | :basil-classic:`#51B749`            | :basil-modern:`#0B8043`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '11'     | Tomato           | :tomato-classic:`#DC2127`           | :tomato-modern:`#D50000`            |
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
.. role:: cocoa-classic
.. role:: cocoa-modern
.. role:: flamingo-classic
.. role:: flamingo-modern
.. role:: tomato-classic
.. role:: tomato-modern
.. role:: tangerine-classic
.. role:: tangerine-modern
.. role:: pumpkin-classic
.. role:: pumpkin-modern
.. role:: mango-classic
.. role:: mango-modern
.. role:: eucalyptus-classic
.. role:: eucalyptus-modern
.. role:: basil-classic
.. role:: basil-modern
.. role:: pistachio-classic
.. role:: pistachio-modern
.. role:: avocado-classic
.. role:: avocado-modern
.. role:: citron-classic
.. role:: citron-modern
.. role:: banana-classic
.. role:: banana-modern
.. role:: sage-classic
.. role:: sage-modern
.. role:: peacock-classic
.. role:: peacock-modern
.. role:: cobalt-classic
.. role:: cobalt-modern
.. role:: blueberry-classic
.. role:: blueberry-modern
.. role:: lavender-classic
.. role:: lavender-modern
.. role:: wisteria-classic
.. role:: wisteria-modern
.. role:: graphite-classic
.. role:: graphite-modern
.. role:: birch-classic
.. role:: birch-modern
.. role:: radicchio-classic
.. role:: radicchio-modern
.. role:: cherry-blossom-classic
.. role:: cherry-blossom-modern
.. role:: grape-classic
.. role:: grape-modern
.. role:: amethyst-classic
.. role:: amethyst-modern

.. table:: Calendar colors
    :widths: 1 1 1 1

    +----------+------------------+-------------------------------------+-------------------------------------+
    | Color ID | Name             | Classic                             |  Modern                             |
    +==========+==================+=====================================+=====================================+
    | '1'      | Cocoa            | :cocoa-classic:`#AC725E`            | :cocoa-modern:`#795548`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '2'      | Flamingo         | :flamingo-classic:`#D06B64`         | :flamingo-modern:`#E67C73`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '3'      | Tomato           | :tomato-classic:`#F83A22`           | :tomato-modern:`#D50000`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '4'      | Tangerine        | :tangerine-classic:`#FA573C`        | :tangerine-modern:`#F4511E`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '5'      | Pumpkin          | :pumpkin-classic:`#FF7537`          | :pumpkin-modern:`#EF6C00`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '6'      | Mango            | :mango-classic:`#FFAD46`            | :mango-modern:`#F09300`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '7'      | Eucalyptus       | :eucalyptus-classic:`#42D692`       | :eucalyptus-modern:`#009688`        |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '8'      | Basil            | :basil-classic:`#16A765`            | :basil-modern:`#0B8043`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '9'      | Pistachio        | :pistachio-classic:`#7BD148`        | :pistachio-modern:`#7CB342`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '10'     | Avocado          | :avocado-classic:`#B3DC6C`          | :avocado-modern:`#C0CA33`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '11'     | Citron           | :citron-classic:`#FBE983`           | :citron-modern:`#E4C441`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '12'     | Banana           | :banana-classic:`#FAD165`           | :banana-modern:`#F6BF26`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '13'     | Sage             | :sage-classic:`#92E1C0`             | :sage-modern:`#33B679`              |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '14'     | Peacock          | :peacock-classic:`#9FE1E7`          | :peacock-modern:`#039BE5`           |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '15'     | Cobalt           | :cobalt-classic:`#9FC6E7`           | :cobalt-modern:`#4285F4`            |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '16'     | Blueberry        | :blueberry-classic:`#4986E7`        | :blueberry-modern:`#3F51B5`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '17'     | Lavender         | :lavender-classic:`#9A9CFF`         | :lavender-modern:`#7986CB`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '18'     | Wisteria         | :wisteria-classic:`#B99AFF`         | :wisteria-modern:`#B39DDB`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '19'     | Graphite         | :graphite-classic:`#C2C2C2`         | :graphite-modern:`#616161`          |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '20'     | Birch            | :birch-classic:`#CABDBF`            | :birch-modern:`#A79B8E`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '21'     | Radicchio        | :radicchio-classic:`#CCA6AC`        | :radicchio-modern:`#AD1457`         |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '22'     | Cherry Blossom   | :cherry-blossom-classic:`#F691B2`   | :cherry-blossom-modern:`#D81B60`    |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '23'     | Grape            | :grape-classic:`#CD74E6`            | :grape-modern:`#8E24AA`             |
    +----------+------------------+-------------------------------------+-------------------------------------+
    | '24'     | Amethyst         | :amethyst-classic:`#A47AE2`         | :amethyst-modern:`#9E69AF`          |
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