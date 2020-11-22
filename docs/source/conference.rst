.. _conference:

Conference
----------

To add conference (such as Hangouts or Google Meet) to an event you can use :py:class:`~gcsa.conference.ConferenceSolution`
(for existing conferences) or :py:class:`~gcsa.conference.ConferenceSolutionCreateRequest` (to create new conference)
and pass it as a ``conference_solution`` parameter:


Existing conference
~~~~~~~~~~~~~~~~~~~

To add existing conference you need to specify its ``solution_type`` (see :py:class:`~gcsa.conference.SolutionType` for
available values) and at least one :py:class:`~gcsa.conference.EntryPoint` in ``entry_points`` parameter. You can pass
single :py:class:`~gcsa.conference.EntryPoint`:

.. code-block:: python


    from gcsa.conference import ConferenceSolution, EntryPoint, SolutionType

    event = Event(
        'Meeting',
        start=(22 / Nov / 2020)[15:00],
        conference_solution=ConferenceSolution(
            entry_points=EntryPoint(
                EntryPoint.VIDEO,
                uri='https://meet.google.com/aaa-bbbb-ccc'
            ),
            solution_type=SolutionType.HANGOUTS_MEET,
        )
    )

or multiple entry points in a list:

.. code-block:: python

    event = Event(
        'Event with conference',
        start=(22 / Nov / 2020)[15:00],
        conference_solution=ConferenceSolution(
            entry_points=[
                EntryPoint(
                    EntryPoint.VIDEO,
                    uri='https://meet.google.com/aaa-bbbb-ccc'
                ),
                EntryPoint(
                    EntryPoint.PHONE,
                    uri='tel:+12345678900'
                )
            ],
            solution_type=SolutionType.HANGOUTS_MEET,
        )
    )

See more parameters for :py:class:`~gcsa.conference.ConferenceSolution` and :py:class:`~gcsa.conference.EntryPoint`.


New conference
~~~~~~~~~~~~~~
To generate new conference you need to specify its ``solution_type`` (see :py:class:`~gcsa.conference.SolutionType` for
available values).

.. code-block:: python


    from gcsa.conference import ConferenceSolutionCreateRequest, SolutionType

    event = Event(
        'Meeting',
        start=(22 / Nov / 2020)[15:00],
        conference_solution=ConferenceSolutionCreateRequest(
            solution_type=SolutionType.HANGOUTS_MEET,
        )
    )

See more parameters for :py:class:`~gcsa.conference.ConferenceSolutionCreateRequest`.

