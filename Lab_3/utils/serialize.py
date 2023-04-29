"""Serialization of Lab_3"""
import re
from collections.abc import Collection
from types import FunctionType, CodeType, NoneType, CellType, MethodType
from typing import Hashable, Iterable, Iterator

from .base import Serializer
from .helpers import Formatter
from .templates import JSON


# TODO *6: Add scope serialization support (+ tests).
# TODO *7: Add library serialization support (+ tests).

# TODO *8: Add XAML serialization templates (+ tests).


class JSONSerializer(Serializer):
    """JSON serializer class."""

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
        elif type(obj) in self._NUMERICS:
            return str(obj)
        elif isinstance(obj, Hashable) and type(obj) in [bool, NoneType]:
            return self._KEYWORDS[obj]

        if isinstance(obj, dict):
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json(obj, self.dumps),
            )
        elif isinstance(obj, Collection):
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json(dict(zip(range(len(obj)), obj)), self.dumps)
            )
        elif isinstance(obj, CodeType):
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json({
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
                }, self.dumps)
            )
        elif isinstance(obj, FunctionType):
            if "__class__" in obj.__code__.co_freevars and obj.__closure__:
                closure = ([... for _ in obj.__closure__])
            else:
                closure = obj.__closure__

            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json({
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
                        for k in set(obj.__globals__) & set(obj.__code__.co_names) - {obj.__name__}
                    },
                    "closure": closure,
                    "qualname": obj.__qualname__
                }, self.dumps),
            )
        elif isinstance(obj, MethodType):
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json({
                    "__func__": obj.__func__,
                    "__self__": obj.__self__
                }, self.dumps)
            )
        elif issubclass(type(obj), type):
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json({
                    'name': obj.__name__,
                    'mro': tuple(obj.mro()[1:-1]),
                    'attrs': {
                        k: v for k, v in obj.__dict__.items()
                        if k not in self._NOT_SERIALIZABLE
                    }
                }, self.dumps)
            )
        else:
            return JSON.format(
                type=object,
                id=id(obj),
                items=Formatter().to_json({
                    'class': obj.__class__,
                    'attrs': {
                        k: v for k, v in obj.__dict__.items()
                        if k not in self._NOT_SERIALIZABLE
                    }
                }, self.dumps)
            )

    # noinspection PyArgumentList,PyUnresolvedReferences
    def loads(self, s: str):
        """Loads an object from a string and returns it.
        Operates using JSON template from ``utils.templates``.
        However, primitive types are serialized without this
        template.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if s == ' ':
            return ...
        if s.startswith('"'):
            return s.strip('"')
        elif s in self._KEYWORDS.values():
            return self._get_key(s, self._KEYWORDS)
        elif self._to_number(s) is not None:
            return self._to_number(s)

        obj_type: type = self._obj_type_from_template(s, r"<class '(\w\S+)'>_")
        obj_data: dict = self._load_from_dictlike_str(s)

        if issubclass(obj_type, dict):
            return obj_data
        elif issubclass(obj_type, Iterable):
            return obj_type(obj_data.values())
        elif issubclass(obj_type, CodeType):
            return CodeType(*list(obj_data.values()))
        elif issubclass(obj_type, FunctionType):
            if obj_data['closure']:
                closure = tuple([CellType(x) for x in obj_data['closure']])
            elif obj_data['closure'] and '__class__' in obj_data['freevars']:
                closure = tuple([CellType(...) for _ in obj_data['closure']])
            else:
                closure = tuple()

            obj = FunctionType(
                code=CodeType(*list(obj_data.values())[:16]),
                globals={
                    **obj_data['globals'],
                    '__builtins__': __builtins__,
                },
                name=obj_data['name'],
                closure=closure
            )
            obj.__qualname__ = obj_data['qualname']
            obj.__globals__[obj.__name__] = obj

            return obj
        elif issubclass(obj_type, MethodType):
            return MethodType(
                obj_data['__func__'],
                obj_data['__self__'],
            )
        elif issubclass(obj_type, type):
            obj = type(obj_data['name'], obj_data['mro'], obj_data['attrs'])
            try:
                obj.__init__.__closure__[0].cell_contents = obj
            except (AttributeError, IndexError):
                ...

            return obj
        else:
            obj = object.__new__(obj_data['class'])
            obj.__dict__ = obj_data['attrs']

            return obj
