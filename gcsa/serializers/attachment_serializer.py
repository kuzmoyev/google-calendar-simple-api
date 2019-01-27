from gcsa.attachment import Attachment
from .base_serializer import BaseSerializer


class AttachmentSerializer(BaseSerializer):
    type_ = Attachment

    def __init__(self, attachment):
        super().__init__(attachment)

    @staticmethod
    def to_json(attachment):
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
    def to_object(json_attachment):
        BaseSerializer.assure_dict(json_attachment)

        return Attachment(
            title=json_attachment['title'],
            file_url=json_attachment['fileUrl'],
            mime_type=json_attachment['mimeType'],
            icon_link=json_attachment.get('iconLink', None),
            file_id=json_attachment.get('fileId', None)
        )
