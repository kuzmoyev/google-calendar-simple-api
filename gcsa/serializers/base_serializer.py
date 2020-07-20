from abc import ABC, abstractmethod
import json


class BaseSerializer(ABC):
    type_ = None

    def __init__(self, obj):
        if isinstance(obj, self.type_):
            self.data = self.to_json(obj)
        elif isinstance(obj, str):
            self.data = json.loads(obj)
        elif isinstance(obj, dict):
            self.data = obj
        else:
            raise TypeError('The "{}" object must be {}, str or dict, not {!r}.'
                            .format(self.type_.__name__.lower(), self.type_.__name__, obj.__class__.__name__))

    def get_object(self):
        return self.to_object(self.data)

    def get_json(self):
        return self.data

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
            raise TypeError('The event object must be {}, not {!r}.'.format(cls.type_, obj.__class__.__name__))

    def __init_subclass__(cls, **kwargs):
        """Checks that "type_" is defined and that name of the argument in subclasses __init__ method is the name of
        the "type_" in lowercase. It assures that error in __init__ function of BaseSerializer has a correct message.
        """
        if cls.type_ is None:
            raise AssertionError('Subclass of BaseSerializer has to define class "type_" that is being serialized.')
        if cls.__init__.__code__.co_varnames != ('self', cls.type_.__name__.lower()):
            raise AssertionError('Argument of the __init__ method has to have a name "{}".'
                                 .format(cls.type_.__name__.lower()))
