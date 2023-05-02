"""Serialization of Lab_3"""
import re
from collections.abc import Collection
from types import (
    FunctionType,
    CodeType,
    NoneType,
    CellType,
    MethodType,
    ModuleType
)
from typing import Hashable, Iterable, Iterator

from .base import Serializer
from .helpers import Formatter
from .templates import JSON


# TODO *6: Add scope serialization support (+ tests).
# TODO *7: Add library serialization support (+ tests).

# TODO *8: Add XAML serialization templates (+ tests).


class JSONSerializer(Serializer):
    """JSON serializer class."""

    _OBJECT_TYPE: str = r"<class '(\w\S+)'>_"

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
        if type(obj) in self._NUMERICS:
            return str(obj)
        if isinstance(obj, Hashable) and type(obj) in [bool, NoneType]:
            return self._KEYWORDS[obj]

        if isinstance(obj, dict):
            items = obj

        elif isinstance(obj, Collection):
            items = dict(enumerate(obj))

        elif isinstance(obj, CodeType):
            items = {
                "argcount": obj.co_argcount,
                "posonlyargcount": obj.co_posonlyargcount,
                "kwonlyargcount": obj.co_kwonlyargcount,
                "nlocals": obj.co_nlocals,
                "stacksize": obj.co_stacksize,
                "flags": obj.co_flags,
                "code": obj.co_code,
                "consts": obj.co_consts,
                "names": obj.co_names,
                "varnames": obj.co_varnames,
                "filename": obj.co_filename,
                "name": obj.co_name,
                "firstlineno": obj.co_firstlineno,
                "lnotab": obj.co_lnotab,
                "freevars": obj.co_freevars,
                "cellvars": obj.co_cellvars,
            }

        elif isinstance(obj, FunctionType):
            if obj.__closure__ and "__class__" in obj.__code__.co_freevars:
                closure = ([... for _ in obj.__closure__])
            else:
                closure = obj.__closure__

            items = {
                "argcount": obj.__code__.co_argcount,
                "posonlyargcount": obj.__code__.co_posonlyargcount,
                "kwonlyargcount": obj.__code__.co_kwonlyargcount,
                "nlocals": obj.__code__.co_nlocals,
                "stacksize": obj.__code__.co_stacksize,
                "flags": obj.__code__.co_flags,
                "code": obj.__code__.co_code,
                "consts": obj.__code__.co_consts,
                "names": obj.__code__.co_names,
                "varnames": obj.__code__.co_varnames,
                "filename": obj.__code__.co_filename,
                "name": obj.__code__.co_name,
                "firstlineno": obj.__code__.co_firstlineno,
                "lnotab": obj.__code__.co_lnotab,
                "freevars": obj.__code__.co_freevars,
                "cellvars": obj.__code__.co_cellvars,
                "globals": {
                    k: obj.__globals__[k]
                    for k in (
                        set(
                            k for k, v in obj.__globals__.items()
                            if isinstance(v, ModuleType)
                        ) |
                        set(obj.__globals__) &
                        set(obj.__code__.co_names) -
                        {obj.__name__}
                    )
                },
                "closure": closure,
                "qualname": obj.__qualname__
            }

        elif isinstance(obj, MethodType):
            items = {
                "__func__": obj.__func__,
                "__self__": obj.__self__
            }

        elif issubclass(type(obj), type):
            items = {
                'name': obj.__name__,
                'mro': tuple(obj.mro()[1:-1]),
                'attrs': {
                    k: v for k, v in obj.__dict__.items()
                    if k not in self._NOT_SERIALIZABLE
                }
            }

        elif issubclass(type(obj), ModuleType):
            items = {'name': obj.__name__}

        else:
            items = {
                'class': obj.__class__,
                'attrs': {
                    k: v for k, v in obj.__dict__.items()
                    if k not in self._NOT_SERIALIZABLE
                }
            }

        return JSON.format(
            type=type(obj),
            id=id(obj),
            items=Formatter().to_json(items, self.dumps)
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
        if s in self._KEYWORDS.values():
            return self._get_key(s, self._KEYWORDS)
        if self._to_number(s) is not None:
            return self._to_number(s)

        obj_type: type = self._obj_type_from_template(s, self._OBJECT_TYPE)
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
    _PRIMITIVE_TYPES: tuple[type] = (int, float, complex, str, bool, NoneType, Ellipsis)
    _TYPE_PATTERN: str = r'type="(\w+)"'
    _PRIMITIVE: str = r'<primitive {type}>{value}</primitive>'

    def dumps(self, obj) -> str:
        if type(obj) in self._PRIMITIVE_TYPES:
            obj_type = re.search(r"<class\s'(\w+)'>", str(type(obj))).group(1)
            return self._PRIMITIVE.format(
                type=f'type="{obj_type}"',
                value=obj
            )

    def loads(self, s):
        if not len(s):
            return

        if re.search(self._PRIMITIVE.format(
                type='type="\w+"',
                value='(.+)'
        ), s):
            obj_data = re.search(self._PRIMITIVE.format(
                type='type="\w+"',
                value='(.+)'
            ), s).group(1)
            obj_type = self._obj_type_from_template(s, self._TYPE_PATTERN)

            if obj_type == NoneType:
                return None
            return obj_type(obj_data)


if __name__ == "__main__":
    xml_ser = XMLSerializer()
    print(type(xml_ser.loads(xml_ser.dumps(True))))
    print(type(xml_ser.loads(xml_ser.dumps("None"))))
    print(type(xml_ser.loads(xml_ser.dumps(None))))
    print(type(xml_ser.loads(xml_ser.dumps("14"))))
    print(type(xml_ser.loads(xml_ser.dumps(14))))
    print(type(xml_ser.loads(xml_ser.dumps("14+9j"))))
    print(type(xml_ser.loads(xml_ser.dumps(14+9j))))
