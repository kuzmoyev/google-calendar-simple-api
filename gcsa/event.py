from tzlocal import get_localzone


class Event:
    def __init__(self,
                 start,
                 end=None,
                 timezone=get_localzone(),
                 event_id=None,
                 summary=None,
                 description=None,
                 location=None,
                 recurrence=None,
                 color=None,
                 visibility=None,
                 gadget=None,
                 attachments=None,
                 reminders=None,
                 default_reminders=True,
                 **other):
        self.start = start
        self.end = end or start
        self.timezone = timezone
        self.event_id = event_id
        self.summary = summary
        self.description = description
        self.location = location
        self.recurrence = recurrence or []
        self.colorId = color
        self.visibility = visibility
        self.gadget = gadget
        self.attachments = attachments or []
        self.reminders = reminders or []
        self.default_reminders = default_reminders
        self.other = other

    def get_id(self):
        return self.event_id

    def add_attachment(self, file_url, title='', mime_type=None, icon_link=None):
        new_attachment = {
            "title": title,
            "fileUrl": file_url,
            "mimeType": mime_type,
            "iconLink": icon_link,
        }
        self.attachments.append(new_attachment)

    def add_email_reminder(self, minutes_before_start=60):
        new_reminder = {
            'method': 'email',
            'minutes': minutes_before_start
        }
        self.reminders.append(new_reminder)

    def add_popup_reminder(self, minutes_before_start=30):
        new_reminder = {
            'method': 'popup',
            'minutes': minutes_before_start
        }
        self.reminders.append(new_reminder)

    def __str__(self):
        return f'{self.start} - {self.summary}'
