# Google Calendar Simple API

[![Build Status](https://travis-ci.com/kuzmoyev/Google-Calendar-Simple-API.svg?branch=master)](https://travis-ci.com/kuzmoyev/Google-Calendar-Simple-API)
[![Documentation Status](https://readthedocs.org/projects/google-calendar-simple-api/badge/?version=latest)](https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest)
  

`Google Calendar Simple API` or `gcsa` is a library that simplifies event management in a Google Calendars.
It is a Pythonic object oriented adapter for the [official API](https://github.com/googleapis/google-api-python-client).


### Installation

    pip install gcsa

### Example usage


    calendar = GoogleCalendar('your_email@gmail.com')
    event = Event(
        'Breakfast',
        start=date(2019, 1, 1),
        recurrence=Recurrence.rule(freq=DAILY)),
        minutes_before_email_reminder=50
    )

    calendar.add_event(event)

    for event in calendar:
        print(event)


See [documentation](https://google-calendar-simple-api.readthedocs.io/en/latest/?badge=latest)
for more parameters and functionality.

**Suggestion**: use [beautiful_date](https://github.com/beautiful-everything/beautiful-date) to creat 
`date` and `datetime` objects in your projects (*because its beautiful... just like you*).


### References

Template for `setup.py` was taken from [kennethreitz/setup.py](https://github.com/kennethreitz/setup.py)
