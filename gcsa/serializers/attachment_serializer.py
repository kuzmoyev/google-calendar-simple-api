from gcsa.attachment import Attachment
from .base_serializer import BaseSerializer


class AttachmentSerializer(BaseSerializer):
    type_ = Attachment

    def __init__(self, attachment):
        super().__init__(attachment)

    @staticmethod
    def _to_json(attachment: Attachment):
        res = {
            "fileUrl": attachment.file_url,
            "title": attachment.title,
            "mimeType": attachment.mime_type,
        }

        if attachment.file_id:
            res['fileId'] = attachment.file_id
        if attachment.icon_link:
            res['iconLink'] = attachment.icon_link

        return res

    @staticmethod
    def _to_object(json_attachment):
        return Attachment(
            file_url=json_attachment['fileUrl'],
            title=json_attachment.get('title', None),
            mime_type=json_attachment.get('mimeType', None),
            _icon_link=json_attachment.get('iconLink', None),
            _file_id=json_attachment.get('fileId', None)
        )
