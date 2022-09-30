.. _change_log:

Change log
==========


v2.0.0
~~~~~~

API
---
* Adds calendar and calendar list related methods
* Adds settings related method
* Adds colors related method
* Adds support for python3.10

Core
----
* Separates ``GoogleCalendar`` into authentication, events, calendars, calendar list, colors, and settings services
* Uses newest documentation generation libraries

Backward compatibility
----------------------
* Full compatibility


v1.3.0
~~~~~~
* Adds deletion of event by its id in ``GoogleCalendar.delete_event()``

Core
----
* None

Backward compatibility
----------------------
* Full compatibility


v1.2.1
~~~~~~
* Adds ``Event.id`` in serialized event
* Fixes conference's entry point without ``entry_point_type``

Core
----
* Switches to tox for testing

Backward compatibility
----------------------
* Full compatibility


v1.2.0
~~~~~~
* Adds ``GoogleCalendar.import_event()`` method

Core
----
* None

Backward compatibility
----------------------
* Full compatibility


v1.1.0
~~~~~~
* Fixes event creation without ``start`` and ``end``
* Adds ``creator``, ``organizer`` and ``transparency`` fields to event

Core
----
* None

Backward compatibility
----------------------
* Full compatibility


v1.0.1
~~~~~~
* Fixes ``GoogleCalendar.clear()`` method

Core
----
* None

Backward compatibility
----------------------
* Full compatibility


v1.0.0 and previous versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Adds authentication management
* Adds event management
* Adds documentation in readthedocs.com

Core
----
* Adds serializers for events and related objects
* Adds automated testing in GitHub actions with code-coverage

Backward compatibility
----------------------
* Full compatibility