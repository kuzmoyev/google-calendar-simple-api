# Google Calendar Simple API

Simple adapter for https://github.com/googleapis/google-api-python-client

Example usege:

    from beautiful_date import *
    from gcsa import GoogleCalendar, Event, rule, DAILY
    
    calendar = GoogleCalendar('kuzmovich.goog@gmail.com')
    event = Event("Breakfast", start=12/Dec/2018, recurrence=rule(freq=DAILY))
    calendar.add_event(event)
    
    ...
    
    for event in calendar:
        print(event.start, event.summary)
        repr(event)  # => <Event 'Breakfast' at 12/Dec/2018>

The idea is to keep all the functionality of the original API, but simplify implementation of the most popular cases, provide Pythonic API:

Front-end:

   - Events management:
      - Pythonic, object-oriented events interface
      - list, create, delete, update, quick add (by string like "Appointment at Somewhere on June 3rd 10am-10:25am" (googles text processing, not mine. Maybe will add some features))
   - Recurrence:
      - Pythonic, object-oriented recurrence interface
   - Simple, intuitive incode documetation

Back-end:

   - Credentials management
   - Timezones management:
      - Assuring timezone on datetime objects
      - Find timezone of the PC and use it as a default
   - Serialization and deserialization of event, recurrence, calendar, ... objects.


![alt tag](http://alfaraj-group.com/wp-content/uploads/2016/09/underConstruction.png)

