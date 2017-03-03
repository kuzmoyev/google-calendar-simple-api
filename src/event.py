class Event:
    def __init__(self,
                 start,
                 end=None,
                 summary=None,
                 description=None,
                 location=None,
                 recurrence=None,
                 color=None,
                 visibility=None,
                 gadget=None,
                 attachments=None,
                 **other):
        self.start = start
        self.end = end or start
        self.summary = summary
        self.description = description
        self.location = location
        self.recurrence = recurrence or []
        self.colorId = color
        self.visibility = visibility
        self.gadget = gadget
        self.reminders = []
        self.attachments = attachments or []
        self.other = other

    def add_attachment(self, file_url, title=''):
        new_attachment = {
            "title": title,
            "fileUrl": file_url,
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
