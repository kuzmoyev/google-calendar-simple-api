.. _authentication:

Authentication
==============

There are several ways to authenticate in ``GoogleCalendar``.

Credentials file
----------------

If you have a ``credentials.json`` (``client_secret_*.json``) file (see :ref:`getting_started`), ``GoogleCalendar``
will read all the needed data to generate the token and refresh-token from it.

To read ``credentials.json`` (``client_secret_*.json``) from the default directory (``~/.credentials``) use:

.. code-block:: python

    gc = GoogleCalendar()

In this case, if ``~/.credentials/token.pickle`` file exists, it will read it and refresh only if needed. If
``token.pickle`` does not exist, it will be created during authentication flow and saved alongside with
``credentials.json`` (``client_secret_*.json``) in ``~/.credentials/token.pickle``.

To **avoid saving** the token use:

.. code-block:: python

    gc = GoogleCalendar(save_token=False)

After token is generated during authentication flow, it can be accessed in ``gc.credentials`` field.

To specify ``credentials.json`` (``client_secret_*.json``) file path use ``credentials_path`` parameter:

.. code-block:: python

    gc = GoogleCalendar(credentials_path='path/to/credentials.json')

or

.. code-block:: python

    gc = GoogleCalendar(credentials_path='path/to/client_secret_273833015691-qwerty.apps.googleusercontent.com.json')

Similarly, if ``token.pickle`` file exists in the same folder (``path/to/``), it will be used and refreshed only if
needed. If it doesn't exist, it will be generated and stored alongside the ``credentials.json`` (``client_secret_*.json``)
(in ``path/to/token.pickle``).

To specify different path for the pickled token file use ``token_path`` parameter:

.. code-block:: python

    gc = GoogleCalendar(credentials_path='path/to/credentials.json',
                        token_path='another/path/user1_token.pickle')

That could be useful if you want to save the file elsewhere, or if you have multiple google accounts.

Token object
------------

If you store/receive/generate the token in a different way, you can pass loaded token directly:

.. code-block:: python

    from google.oauth2.credentials import Credentials

    token = Credentials(
        token='<access_token>',
        refresh_token='<refresh_token>',
        client_id='<client_id>',
        client_secret='<client_secret>',
        scopes=['https://www.googleapis.com/auth/calendar'],
        token_uri='https://oauth2.googleapis.com/token'
    )
    gc = GoogleCalendar(credentials=token)

It will be refreshed using ``refresh_token`` during initialization of ``GoogleCalendar`` if needed.


Multiple calendars
------------------
To authenticate multiple Google Calendars you should specify different `token_path` for each of them. Otherwise,
`gcsa` would overwrite default token file location:

.. code-block:: python

    gc_primary = GoogleCalendar(token_path='path/to/tokens/token_primary.pickle')
    gc_secondary = GoogleCalendar(calendar='f7c1gf7av3g6f2dave17gan4b8@group.calendar.google.com',
                                  token_path='path/to/tokens/token_secondary.pickle')


Browser authentication timeout
------------------------------

If you'd like to avoid your script hanging in case user closes the browser without finishing authentication flow,
you can use the following solution with the help of Pebble_.

First, install `Pebble` with ``pip install pebble``.

.. code-block:: python

    from gcsa.google_calendar import GoogleCalendar
    from concurrent.futures import TimeoutError
    from pebble import concurrent


    @concurrent.process(timeout=60)
    def create_process():
        return GoogleCalendar()


    if __name__ == '__main__':
        try:
            process = create_process()
            gc = process.result()
        except TimeoutError:
            print("User hasn't authenticated in 60 seconds")

Thanks to Teraskull_ for the idea and the example.

.. _Pebble: https://pypi.org/project/Pebble/
.. _Teraskull: https://github.com/Teraskull

