class Attachment:
    _SUPPORTED_MIME_TYPES = [
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
    ]

    def __init__(self, title, file_url, mime_type, icon_link=None, file_id=None):
        """File attachment for the event.

        Currently only Google Drive attachments are supported.

        :param title:
                attachment title
        :param file_url:
                a link for opening the file in a relevant Google editor or viewer.
        :param mime_type:
                internet media type (MIME type) of the attachment. See  `available MIME types`_
        :param icon_link:
                URL link to the attachment's icon (read only)
        :param file_id:
                id of the attached file (read only)

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
