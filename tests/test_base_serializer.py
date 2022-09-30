from unittest import TestCase

from gcsa.serializers.base_serializer import BaseSerializer


class TestBaseSerializer(TestCase):
    def test_ensure_dict(self):
        json_str = """
        {
            "key": "value",
            "list": [1, 2, 4]
        }
        """

        json_dict = {
            "key": "value",
            "list": [1, 2, 4]
        }

        json_object = (1, 2, 3)  # non-json object

        self.assertDictEqual(BaseSerializer.ensure_dict(json_str), json_dict)
        self.assertDictEqual(BaseSerializer.ensure_dict(json_dict), json_dict)

        with self.assertRaises(TypeError):
            BaseSerializer.ensure_dict(json_object)

    def test_subclass(self):
        class Apple:
            pass

        # should not raise any exceptions
        class AppleSerializer(BaseSerializer):
            type_ = Apple

            def __init__(self, apple):
                super().__init__(apple)

            @staticmethod
            def _to_json(obj):
                pass

            @staticmethod
            def _to_object(json_):
                pass

        with self.assertRaises(AssertionError):
            # type_ not defined
            class PeachSerializer(BaseSerializer):
                def __init__(self, peach):
                    super().__init__(peach)

                @staticmethod
                def _to_json(obj):
                    pass

                @staticmethod
                def _to_object(json_):
                    pass

        class Watermelon:
            pass

        with self.assertRaises(AssertionError):
            # __init__ parameter should be "apple"
            class WatermelonSerializer(BaseSerializer):
                type_ = Watermelon

                def __init__(self, peach):
                    super().__init__(peach)

                @staticmethod
                def _to_json(obj):
                    pass

                @staticmethod
                def _to_object(json_):
                    pass

        with self.assertRaises(TypeError):
            AppleSerializer(Watermelon)

        with self.assertRaises(TypeError):
            AppleSerializer.to_json(Watermelon)
