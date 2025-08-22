from typing import List, Iterable, Type, Tuple, Optional


def ensure_list(obj) -> List:
    if obj is None:
        return []
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]


def ensure_iterable(obj) -> Iterable:
    if obj is None:
        return []
    elif isinstance(obj, (list, tuple, set)):
        return obj
    else:
        return [obj]


def check_all_type(it: Iterable, type_: Type, name: str):
    """Checks that all objects in `it` are of type `type_`."""
    if any(not isinstance(o, type_) for o in it):
        raise TypeError('"{}" parameter must be a {} or list of {}s.'
                        .format(name, type_.__name__, type_.__name__))


def check_all_type_and_range(it: Iterable, type_: Type, range_: Tuple[int, int], name: str, nonzero: bool = False):
    """Checks that all objects in `it` are of type `type_` and they are within `range_`"""
    check_all_type(it, type_, name)
    low, high = range_
    if any(not (low <= o <= high) for o in it):
        raise ValueError('"{}" parameter must be in range {}-{}.'
                         .format(name, low, high))
    if nonzero and any(o == 0 for o in it):
        raise ValueError('"{}" parameter must be in range {}-{} and nonzero.'
                         .format(name, low, high))


def to_string(values: Optional[Iterable]):
    return ','.join(map(str, values)) if values else None
