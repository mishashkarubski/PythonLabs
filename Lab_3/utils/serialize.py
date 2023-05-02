"""Serialization of Lab_3"""
import re
from types import (
    FunctionType,
    CodeType,
    NoneType,
    CellType,
    MethodType,
    ModuleType
)
from typing import Iterable, Iterator

from .base import Serializer
from .helpers import Formatter
from .templates import JSON, XML, XML_PRIMITIVE
from .contants import PRIMITIVE_TYPES

# TODO *8: Add XAML serialization templates (+ tests).


class JSONSerializer(Serializer):
    """JSON serializer class."""
    _TYPE_PATTERN: str = r"<class '(\w\S+)'>_"

    def __init__(self):
        super().__init__()

    def _load_from_dictlike_str(self, template: str) -> dict:
        """Takes a string of specific format (visit ``utils.templates``
        for more clarity) as an input, loads object data,
        and returns it in the form of dict.

        :param template: string template to retrieve object from.
        :return: dictionary with object data.
        """
        obj: dict = {}
        lines: list[str] = template.split("\n")
        it: Iterator[str] = enumerate(lines)

        for i, line in it:
            if not re.search(r'\s*(.+):\s*([^,]*)', line):
                continue

            key, value = re.search(r'\s*(.+):\s*([^,]*)', line).groups()

            if value != "{":
                obj[self.loads(key)] = self.loads(value)

            elif value == "{" and "<class" not in key:
                brackets = 1
                start = i + 1

                while brackets and i < len(lines) - 1:
                    i, line = next(it, None)
                    brackets += ("{" in lines[i]) - ("}" in lines[i])

                obj[self.loads(key)] = self.loads('\n'.join(lines[start:i]))

        return obj

    def dumps(self, obj) -> str:
        """Dumps an object to a string and returns the string.
        Dumping is done via general JSON object template. It can
        overcomplicate simple structure serialization, but can be
        applied to much larger scale of python objects.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        if type(obj) == str:
            return f'"{obj}"'
        if type(obj) == type(Ellipsis):
            return ' '
        if type(obj) in (int, float, complex):
            return str(obj)
        if type(obj) in [bool, NoneType]:
            return self._JSON_KEYWORDS[obj]

        return JSON.format(
            type=type(obj),
            id=id(obj),
            items=Formatter().to_json(self.get_items(obj), self.dumps)
        )

    # noinspection PyArgumentList,PyUnresolvedReferences
    def loads(self, s: str):
        """Loads an object from a string and returns it.
        Operates using JSON template from ``utils.templates``.
        However, primitive types are serialized without this
        or any other template.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if s == ' ':
            return ...
        if s.startswith('"'):
            return s.strip('"')
        if s in self._JSON_KEYWORDS.values():
            return self._get_key(s, self._JSON_KEYWORDS)
        if self._to_number(s) is not None:
            return self._to_number(s)

        obj_type: type = self._obj_type_from_template(s, self._TYPE_PATTERN)
        obj_items: dict = self._load_from_dictlike_str(s)

        if issubclass(obj_type, dict):
            return obj_items

        elif issubclass(obj_type, Iterable):
            return obj_type(obj_items.values())

        elif issubclass(obj_type, CodeType):
            return CodeType(*list(obj_items.values()))

        elif issubclass(obj_type, FunctionType):
            if obj_items.get('closure'):
                closure = tuple([CellType(x) for x in obj_items.get('closure')])
            elif obj_items.get('closure') and '__class__' in obj_items.get('freevars'):
                closure = tuple([CellType(...) for _ in obj_items.get('closure')])
            else:
                closure = tuple()

            obj = FunctionType(
                code=CodeType(*list(obj_items.values())[:16]),
                globals=obj_items.get('globals'),
                name=obj_items['name'],
                closure=closure
            )
            obj.__qualname__ = obj_items.get('qualname')
            obj.__globals__[obj.__name__] = obj

            return obj

        elif issubclass(obj_type, MethodType):
            return MethodType(
                obj_items.get('__func__'),
                obj_items.get('__self__'),
            )

        elif issubclass(obj_type, type):
            obj = type(obj_items.get('name'), obj_items.get('mro'), obj_items.get('attrs'))

            try:
                obj.__init__.__closure__[0].cell_contents = obj
            except (AttributeError, IndexError):
                ...

            return obj

        elif issubclass(obj_type, ModuleType):
            return __import__(obj_items.get('name'))

        else:
            obj = object.__new__(obj_items['class'])
            obj.__dict__ = obj_items.get('attrs')

            return obj


class XMLSerializer(Serializer):
    _TYPE_PATTERN: str = r'type="(\w+)"'

    def dumps(self, obj) -> str:
        """Dumps an object to a string and returns the string.
        Dumping is done via string templates with XML prefix in
        ``utils.templates`` module.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        if type(obj) in PRIMITIVE_TYPES:
            obj_type = self._get_key(type(obj), self._TYPE_MAPPING)
            return f'<primitive type="{obj_type}">{obj}</primitive>'

        return XML.format(
            type=self._get_key(type(obj), self._TYPE_MAPPING),
            id=id(obj),
            items=Formatter().to_xml(self.get_items(obj), self.dumps)
        )

    def loads(self, s):
        """Loads an object from a string and returns it.

        Operates using templates with XML prefix from ``utils.templates``.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if "primitive" in s.split("\n")[0]:
            obj_data = re.search(XML_PRIMITIVE, s).group(1)
            obj_type = self._obj_type_from_template(
                s.split("\n")[0],
                self._TYPE_PATTERN
            )

            if obj_type == NoneType:
                return None
            return obj_type(obj_data)

        # if "object" in s.split("\n")[0]:
        #     ...

