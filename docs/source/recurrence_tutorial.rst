Recurrence
==========

With ``gcsa`` you can create recurrent events. Use :py:mod:`~gcsa.recurrence` module.

There are 8 methods that you can use to define recurrence rules:

    * :py:meth:`~gcsa.recurrence.Recurrence.rule` - rule that defines recurrence
    * :py:meth:`~gcsa.recurrence.Recurrence.exclude_rule` - rule that defines excluded dates/datetimes
    * :py:meth:`~gcsa.recurrence.Recurrence.dates` - date or list of dates to include
    * :py:meth:`~gcsa.recurrence.Recurrence.exclude_dates` - date or list of dates to exclude
    * :py:meth:`~gcsa.recurrence.Recurrence.times` - datetime or list of datetimes to include
    * :py:meth:`~gcsa.recurrence.Recurrence.exclude_times` - datetime or list of datetimes to exclude
    * :py:meth:`~gcsa.recurrence.Recurrence.periods` - period or list of periods to include
    * :py:meth:`~gcsa.recurrence.Recurrence.exclude_periods` - period or list of periods to exclude

.. note:: Methods ``{method}`` have the same format and parameters as their ``exclude_{method}``
    counterparts. So all examples for ``{method}`` also apply to ``exclude_{method}``.

These methods return strings in ``RRULE`` format that you can pass as a ``recurrence`` parameter
to the :py:class:`~gcsa.event.Event` objects. You can pass one string or list of strings.
For example:

.. code-block:: python

   Event('Breakfast',
         (1/Jan/2019)[9:00],
         (1/Jan/2020)[9:00],
         recurrence=Recurrence.rule(freq=DAILY))

or

.. code-block:: python

   Event('Breakfast',
         (1/Jan/2019)[9:00],
         (1/Jan/2020)[9:00],
         recurrence=[
            Recurrence.rule(freq=DAILY),
            Recurrence.exclude_rule(by_week_day=[SU, SA])
         ])



Examples
--------

You will need to import :py:class:`~gcsa.recurrence.Recurrence` class and optionally other
auxiliary classes and objects:

.. code-block:: python

    from gcsa.recurrence import Recurrence

    # days of the week
    from gcsa.recurrence import SU, MO, TU, WE, TH, FR, SA

    # possible repetition frequencies
    from gcsa.recurrence import SECONDLY, MINUTELY, HOURLY, \
                                DAILY, WEEKLY, MONTHLY, YEARLY



Examples were taken from the `Internet Calendaring and Scheduling Core Object Specification (iCalendar)`_
and adapted to ``gcsa``.


:py:meth:`~gcsa.recurrence.Recurrence.rule` and :py:meth:`~gcsa.recurrence.Recurrence.exclude_rule`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Daily for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=DAILY, count=10)

or as ``DAILY`` is a default frequency:

.. code-block:: python

    Recurrence.rule(count=10)


`Every other day`:

.. code-block:: python

    Recurrence.rule(freq=DAILY, interval=2)


`Every 10 days, 5 occurrences`:

.. code-block:: python

    Recurrence.rule(count=5, interval=10)


`Every day in January`:

.. code-block:: python

    Recurrence.rule(freq=YEARLY,
                    by_month=1,
                    by_week_day=[SU,MO,TU,WE,TH,FR,SA])

or

.. code-block:: python

    Recurrence.rule(freq=DAILY, by_month=1)


`Weekly for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=WEEKLY, count=10)

`Weekly on Tuesday and Thursday`:

.. code-block:: python

    Recurrence.rule(freq=WEEKLY,
                    by_week_day=[TU, TH])

`Every other week on Monday, Wednesday, and Friday`:

.. code-block:: python

    Recurrence.rule(freq=WEEKLY,
                    interval=2,
                    by_week_day=[MO, WE, FR])


`Every other week on Tuesday and Thursday, for 8 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=WEEKLY,
                    interval=2,
                    count=8,
                    by_week_day=[TU, TH])

`Monthly on the first Friday for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    count=10,
                    by_week_day=FR(1))

`Every other month on the first and last Sunday of the month for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    interval=2,
                    count=10,
                    by_week_day=[SU(1), SU(-1)])


`Monthly on the second-to-last Monday of the month for 6 months`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    count=6,
                    by_week_day=MO(-2))


`Monthly on the third-to-the-last day of the month`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    by_month_day=-3)


`Monthly on the 2nd and 15th of the month for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    count=10,
                    by_month_day=[2, 15])


`Monthly on the first and last day of the month for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    count=10,
                    by_month_day=[1, -1])

`Every 18 months on the 10th thru 15th of the month for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    interval=18,
                    count=10,
                    by_month_day=list(range(10, 16)))


`Every Tuesday, every other month`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    interval=2,
                    by_week_day=TU)


`Yearly in June and July for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=YEARLY,
                    count=10,
                    by_month=[6, 7])


`Every third year on the 1st, 100th, and 200th day for 10 occurrences`:

.. code-block:: python

    Recurrence.rule(freq=YEARLY,
                    interval=3,
                    count=10,
                    by_year_day=[1, 100, 200])


`Every 20th Monday of the year`:

.. code-block:: python

    Recurrence.rule(freq=YEARLY,
                    by_week_day=MO(20))


`Monday of week number 20 (where the default start of the week is Monday)`:

.. code-block:: python

    Recurrence.rule(freq=YEARLY,
                    by_week=20,
                    week_start=MO)


`Every Thursday in March`:

.. code-block:: python

    Recurrence.rule(freq=YEARLY,
                    by_month=3,
                    by_week_day=TH)


`The third instance into the month of one of Tuesday, Wednesday, or
Thursday, for the next 3 months`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    count=3,
                    by_week_day=[TU, WE, TH],
                    by_set_pos=3)


`The second-to-last weekday of the month`:

.. code-block:: python

    Recurrence.rule(freq=MONTHLY,
                    by_week_day=[MO, TU, WE, TH, FR],
                    by_set_pos=-2)


`Every 20 minutes from 9:00 AM to 4:40 PM every day`:

.. code-block:: python

    Recurrence.rule(freq=DAILY,
                    by_hour=list(range(9, 17)),
                    by_minute=[0, 20, 40])


.. _`Internet Calendaring and Scheduling Core Object Specification (iCalendar)`: https://tools.ietf.org/html/rfc5545#section-3.8.5
