from unittest import TestCase

from gcsa.attachment import Attachment
from gcsa.serializers.attachment_serializer import AttachmentSerializer

DOC_URL = 'https://docs.google.com/document/d/1uDvwcxOsXkzl2Bod0YIfrIQ5MqfBhnc1jusYdH1xCZo/edit?usp=sharing'


class TestAttachment(TestCase):

    def test_create(self):
        attachment = Attachment('My doc',
                                file_url=DOC_URL,
                                mime_type="application/vnd.google-apps.document")
        self.assertEqual(attachment.title, 'My doc')

        with self.assertRaises(ValueError):
            Attachment('My doc',
                       file_url=DOC_URL,
                       mime_type="application/vnd.google-apps.something")


class TestAttachmentSerializer(TestCase):

    def test_to_json(self):
        attachment = Attachment('My doc',
                                file_url=DOC_URL,
                                mime_type="application/vnd.google-apps.document")
        attachment_json = {
            'title': 'My doc',
            'fileUrl': DOC_URL,
            'mimeType': "application/vnd.google-apps.document"
        }
        self.assertDictEqual(AttachmentSerializer.to_json(attachment), attachment_json)

        attachment = Attachment('My doc2',
                                file_url=DOC_URL,
                                mime_type="application/vnd.google-apps.drawing",
                                icon_link="https://some_link.com",
                                file_id='abc123')
        attachment_json = {
            'title': 'My doc2',
            'fileUrl': DOC_URL,
            'mimeType': "application/vnd.google-apps.drawing",
            'iconLink': "https://some_link.com",
            'fileId': 'abc123'
        }
        self.assertDictEqual(AttachmentSerializer.to_json(attachment), attachment_json)

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
        attachment = AttachmentSerializer.to_object(attachment_json)

        self.assertEqual(attachment.title, 'My doc2')
        self.assertEqual(attachment.file_url, DOC_URL)
        self.assertEqual(attachment.mime_type, "application/vnd.google-apps.drawing")
        self.assertEqual(attachment.icon_link, "https://some_link.com")
        self.assertEqual(attachment.file_id, 'abc123')
