from unittest import TestCase

from gcsa.gadget import Gadget
from gcsa.serializers.gadget_serializer import GadgetSerializer


class TestGadget(TestCase):
    def test_init(self):
        required_args = {
            "type_": 'gadget',
            "link": 'https://gadgets_url.com',
            "icon_link": 'https://icons_url.com'
        }
        gadget = Gadget('My gadget',
                        **required_args,
                        display=Gadget.ICON,
                        height=50,
                        width=50)
        self.assertEqual(gadget.title, 'My gadget')
        self.assertEqual(gadget.height, 50)

        with self.assertRaises(ValueError):
            Gadget('', **required_args)
        with self.assertRaises(ValueError):
            Gadget('My gadget', **required_args, display='apple')
        with self.assertRaises(ValueError):
            Gadget('My gadget', **required_args, height=0)
        with self.assertRaises(ValueError):
            Gadget('My gadget', **required_args, width=-5)


class TestGadgetSerializer(TestCase):
    def test_to_json(self):
        required_args = {
            "type_": 'gadget',
            "link": 'https://gadgets_url.com',
            "icon_link": 'https://icons_url.com'
        }
        gadget = Gadget('My gadget',
                        **required_args,
                        display=Gadget.ICON,
                        height=50,
                        width=50)

        gadget_json = {
            "title": 'My gadget',
            "type": 'gadget',
            "link": 'https://gadgets_url.com',
            "iconLink": 'https://icons_url.com',
            "display": Gadget.ICON,
            "height": 50,
            "width": 50,
            "preferences": {}
        }
        self.assertDictEqual(GadgetSerializer.to_json(gadget), gadget_json)

        gadget = Gadget('My gadget', **required_args)

        gadget_json = {
            "title": 'My gadget',
            "type": 'gadget',
            "link": 'https://gadgets_url.com',
            "iconLink": 'https://icons_url.com',
            "preferences": {}
        }
        self.assertDictEqual(GadgetSerializer.to_json(gadget), gadget_json)

    def test_to_object(self):
        gadget_json = {
            "title": 'My gadget',
            "type": 'gadget',
            "link": 'https://gadgets_url.com',
            "iconLink": 'https://icons_url.com',
            "display": Gadget.CHIP,
            "height": 50,
            "width": 50,
            "preferences": {}
        }

        gadget = GadgetSerializer.to_object(gadget_json)

        self.assertEqual(gadget.title, 'My gadget')
        self.assertEqual(gadget.type_, 'gadget')
        self.assertEqual(gadget.link, 'https://gadgets_url.com')
        self.assertEqual(gadget.icon_link, 'https://icons_url.com')
        self.assertEqual(gadget.display, Gadget.CHIP)
        self.assertEqual(gadget.height, 50)
        self.assertEqual(gadget.width, 50)

        gadget_json = {
            "title": 'My gadget',
            "type": 'gadget',
            "link": 'https://gadgets_url.com',
            "iconLink": 'https://icons_url.com',
        }

        gadget = GadgetSerializer.to_object(gadget_json)

        self.assertEqual(gadget.title, 'My gadget')
        self.assertEqual(gadget.type_, 'gadget')
        self.assertEqual(gadget.link, 'https://gadgets_url.com')
        self.assertEqual(gadget.icon_link, 'https://icons_url.com')
        self.assertIsNone(gadget.display)
        self.assertIsNone(gadget.height)
        self.assertIsNone(gadget.width)
