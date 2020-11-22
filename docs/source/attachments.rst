.. _attachments:

Attachments
-----------

If you want to add attachment(s) to your event, just create :py:class:`~gcsa.attachment.Attachment` (s) and pass
as a ``attachments`` parameter:

.. code-block:: python

    from gcsa.attachment import Attachment

    attachment = Attachment('My file',
                            file_url='https://bit.ly/3lZo0Cc',
                            mime_type='application/vnd.google-apps.document')

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  attachments=attachment)


You can pass multiple attachments at once in a list.

.. code-block:: python

    event = Event('Meeting',
                  start=(22/Apr/2019)[12:00],
                  attachments=[attachment1, attachment2])

