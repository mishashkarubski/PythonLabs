"""Metaclass method"""
from Lab_3.utils.serialization import (
    dump,
    dumps,
    load,
    loads
)


def create_serializer(name: str, bases: tuple, attrs: dict):
    """Factory method for creating serializers"""

    attrs.update({
        'dump': dump,
        'dumps': dumps,
        'load': load,
        'loads': loads
    })

    return type(name, bases, attrs)
