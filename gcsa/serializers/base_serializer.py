import re
from abc import ABC, abstractmethod
import json


def _type_to_snake_case(type_):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', type_.__name__).lower()


class BaseSerializer(ABC):
    type_ = None

    def __init__(self, obj):
        if isinstance(obj, self.type_):
            self.obj = obj
        elif isinstance(obj, (str, dict)):
            self.obj = self.to_object(obj)
        else:
            raise TypeError('The "{}" object must be {}, str or dict, not {!r}.'
                            .format(_type_to_snake_case(self.type_), self.type_.__name__, obj.__class__.__name__))

    def get_object(self):
        return self.obj

    def get_json(self):
        return self.to_json(self.obj)

    @staticmethod
    def _remove_empty_values(data):
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def to_json(cls, obj):
        cls.assure_type(obj)
        return cls._to_json(obj)

    @staticmethod
    @abstractmethod
    def _to_json(obj):
        pass

    @classmethod
    def to_object(cls, json_):
        json_ = cls.assure_dict(json_)
        return cls._to_object(json_)

    @staticmethod
    @abstractmethod
    def _to_object(json_):
        pass

    @staticmethod
    def assure_dict(json_):
        if not isinstance(json_, (str, dict)):
            raise TypeError('The json object must be str or dict, not {!r}'.format(json_.__class__.__name__))

        if isinstance(json_, str):
            return json.loads(json_)
        else:
            return json_

    @classmethod
    def assure_type(cls, obj):
        if not isinstance(obj, cls.type_):
            raise TypeError('The object must be {}, not {!r}.'.format(cls.type_, obj.__class__.__name__))

    def __init_subclass__(cls, **kwargs):
        """Checks that "type_" is defined and that name of the argument in subclasses __init__ method is the name of
        the "type_" in lowercase. It assures that error in __init__ function of BaseSerializer has a correct message.
        """
        if cls.type_ is None:
            raise AssertionError('Subclass of BaseSerializer has to define class "type_" that is being serialized.')
        if cls.__init__.__code__.co_varnames != ('self', _type_to_snake_case(cls.type_)):
            raise AssertionError('Argument of the __init__ method has to have a name "{}".'
                                 .format(_type_to_snake_case(cls.type_)))
