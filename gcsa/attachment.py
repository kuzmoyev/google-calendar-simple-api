class Attachment:
    _SUPPORTED_MIME_TYPES = {
        "application/vnd.google-apps.audio",
        "application/vnd.google-apps.document",  # Google Docs
        "application/vnd.google-apps.drawing",  # Google Drawing
        "application/vnd.google-apps.file",  # Google Drive file
        "application/vnd.google-apps.folder",  # Google Drive folder
        "application/vnd.google-apps.form",  # Google Forms
        "application/vnd.google-apps.fusiontable",  # Google Fusion Tables
        "application/vnd.google-apps.map",  # Google My Maps
        "application/vnd.google-apps.photo",
        "application/vnd.google-apps.presentation",  # Google Slides
        "application/vnd.google-apps.script",  # Google Apps Scripts
        "application/vnd.google-apps.site",  # Google Sites
        "application/vnd.google-apps.spreadsheet",  # Google Sheets
        "application/vnd.google-apps.unknown",
        "application/vnd.google-apps.video",
        "application/vnd.google-apps.drive-sdk"  # 3rd party shortcut
    }

    def __init__(self, title, file_url, mime_type, icon_link=None, file_id=None):
        """File attachment for the event.

        Currently only Google Drive attachments are supported.

        :param title:
                Attachment title
        :param file_url:
                A link for opening the file in a relevant Google editor or viewer.
        :param mime_type:
                Internet media type (MIME type) of the attachment. See  `available MIME types`_
        :param icon_link:
                URL link to the attachment's icon (read only)
        :param file_id:
                Id of the attached file (read only)

        .. note: "read only" means that Attachment has given property only
                 when received from the existing event in the calendar.

        .. _`available MIME types`: https://developers.google.com/drive/api/v3/mime-types
        """

        if mime_type not in Attachment._SUPPORTED_MIME_TYPES:
            raise ValueError("Mime type {} is not supported.".format(mime_type))

        self.title = title
        self.file_url = file_url
        self.mime_type = mime_type
        self.icon_link = icon_link
        self.file_id = file_id

    def __eq__(self, other):
        return (
                isinstance(other, Attachment)
                and self.title == other.title
                and self.file_url == other.file_url
                and self.mime_type == other.mime_type
                and self.icon_link == other.icon_link
                and self.file_id == other.file_id
        )

    def __str__(self):
        return "'{}' - '{}'".format(self.title, self.file_url)

    def __repr__(self):
        return '<Attachment {}>'.format(self.__str__())
