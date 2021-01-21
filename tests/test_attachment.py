from unittest import TestCase

from gcsa.attachment import Attachment
from gcsa.serializers.attachment_serializer import AttachmentSerializer

DOC_URL = 'https://bit.ly/3lZo0Cc'


class TestAttachment(TestCase):

    def test_create(self):
        attachment = Attachment(
            file_url=DOC_URL,
            title='My doc',
            mime_type="application/vnd.google-apps.document"
        )
        self.assertEqual(attachment.title, 'My doc')

        attachment = Attachment(
                file_url=DOC_URL,
                title='My doc',
                mime_type="application/vnd.google-apps.something"
            )
        self.assertTrue(attachment.unsupported_mime_type)

    def test_repr_str(self):
        attachment = Attachment(
            file_url=DOC_URL,
            title='My doc',
            mime_type="application/vnd.google-apps.document"
        )
        self.assertEqual(attachment.__repr__(), "<Attachment 'My doc' - 'https://bit.ly/3lZo0Cc'>")
        self.assertEqual(attachment.__str__(), "'My doc' - 'https://bit.ly/3lZo0Cc'")


class TestAttachmentSerializer(TestCase):

    def test_to_json(self):
        attachment = Attachment(
            file_url=DOC_URL,
            title='My doc',
            mime_type="application/vnd.google-apps.document"
        )
        attachment_json = {
            'title': 'My doc',
            'fileUrl': DOC_URL,
            'mimeType': "application/vnd.google-apps.document"
        }
        self.assertDictEqual(AttachmentSerializer.to_json(attachment), attachment_json)

        attachment = Attachment(
            file_url=DOC_URL,
            title='My doc2',
            mime_type="application/vnd.google-apps.drawing",
            _icon_link="https://some_link.com",
            _file_id='abc123'
        )
        attachment_json = {
            'title': 'My doc2',
            'fileUrl': DOC_URL,
            'mimeType': "application/vnd.google-apps.drawing",
            'iconLink': "https://some_link.com",
            'fileId': 'abc123'
        }
        serializer = AttachmentSerializer(attachment)
        self.assertDictEqual(serializer.get_json(), attachment_json)

    def test_to_object(self):
        attachment_json = {
            'title': 'My doc',
            'fileUrl': DOC_URL,
            'mimeType': "application/vnd.google-apps.document"
        }
        attachment = AttachmentSerializer.to_object(attachment_json)

        self.assertEqual(attachment.title, 'My doc')
        self.assertEqual(attachment.file_url, DOC_URL)
        self.assertEqual(attachment.mime_type, "application/vnd.google-apps.document")
        self.assertIsNone(attachment.icon_link)
        self.assertIsNone(attachment.file_id)

        attachment_json = {
            'title': 'My doc2',
            'fileUrl': DOC_URL,
            'mimeType': "application/vnd.google-apps.drawing",
            'iconLink': "https://some_link.com",
            'fileId': 'abc123'
        }
        serializer = AttachmentSerializer(attachment_json)
        attachment = serializer.get_object()

        self.assertEqual(attachment.title, 'My doc2')
        self.assertEqual(attachment.file_url, DOC_URL)
        self.assertEqual(attachment.mime_type, "application/vnd.google-apps.drawing")
        self.assertEqual(attachment.icon_link, "https://some_link.com")
        self.assertEqual(attachment.file_id, 'abc123')

        attachment_json_str = """{
            "title": "My doc3",
            "fileUrl": "%s",
            "mimeType": "application/vnd.google-apps.drawing",
            "iconLink": "https://some_link.com",
            "fileId": "abc123"
        }
        """ % DOC_URL
        attachment = AttachmentSerializer.to_object(attachment_json_str)

        self.assertEqual(attachment.title, 'My doc3')
        self.assertEqual(attachment.file_url, DOC_URL)
        self.assertEqual(attachment.mime_type, "application/vnd.google-apps.drawing")
        self.assertEqual(attachment.icon_link, "https://some_link.com")
        self.assertEqual(attachment.file_id, 'abc123')
