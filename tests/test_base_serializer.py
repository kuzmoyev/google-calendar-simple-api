from unittest import TestCase

from gcsa.serializers.base_serializer import BaseSerializer


class TestBaseSerializer(TestCase):
    def test_init(self):
        pass

    def test_assure_dict(self):
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

        self.assertDictEqual(BaseSerializer.assure_dict(json_str), json_dict)
        self.assertDictEqual(BaseSerializer.assure_dict(json_dict), json_dict)

        with self.assertRaises(TypeError):
            BaseSerializer.assure_dict(json_object)

    def test_subclass(self):
        # __init_subclass__ was introduced in Python 3.6
        # In older versions tests are not executed
        import sys
        if sys.version_info[1] < 6:
            return

        class Apple:
            pass

        # should not raise any exceptions
        class AppleSerializer(BaseSerializer):
            type_ = Apple

            def __init__(self, apple):
                super().__init__(apple)

        with self.assertRaises(AssertionError):
            # type_ not defined
            class PeachSerializer(BaseSerializer):
                def __init__(self, peach):
                    super().__init__(peach)

        with self.assertRaises(AssertionError):
            class Watermelon:
                pass

            # __init__ parameter should be "apple"
            class WatermelonSerializer(BaseSerializer):
                type_ = Watermelon

                def __init__(self, peach):
                    super().__init__(peach)
