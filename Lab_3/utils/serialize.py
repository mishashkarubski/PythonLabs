"""Serialization of Lab_3"""
import re
from collections.abc import Collection
from types import FunctionType, CodeType, NoneType
from typing import Hashable, Iterable, Iterator

from .base import Serializer
from .helpers import Formatter
from .templates import JSON


# TODO *3: Add globals and closures support for function serialization (+ tests).
# TODO *4: Add method serialization support (+ tests).
# TODO *5: Add class & object serialization support (+ tests).
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

        for i, l in it:
            if not re.search(r'\s*(.+):\s*([^,]*)', l):
                continue

            key, value = re.search(r'\s*(.+):\s*([^,]*)', l).groups()

            if value != "{":
                obj[self.loads(key)] = self.loads(value)

            elif value == "{" and "class" not in key:
                n_lines = ["}" in line for line in lines[i+1:]].index(True) + 2
                obj[self.loads(key)] = self.loads('\n'.join(lines[i+1:i+n_lines]))
                [next(it, None) for _ in range(n_lines)]

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

        if isinstance(obj, Collection):
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json(dict(zip(range(len(obj)), obj)), self.dumps)
            )

        if isinstance(obj, FunctionType):
            func_code = {
                "argcount": obj.__code__.co_argcount,
                "posonlyargcount": obj.__code__.co_posonlyargcount,
                "kwonlyargcount": obj.__code__.co_kwonlyargcount,
                "nlocals": obj.__code__.co_nlocals,
                "stacksize": obj.__code__.co_stacksize,
                "flags": obj.__code__.co_flags,
                "code": obj.__code__.co_code.decode('unicode-escape'),
                "consts": obj.__code__.co_consts,
                "names": obj.__code__.co_names,
                "varnames": obj.__code__.co_varnames,
                "filename": obj.__code__.co_filename,
                "name": obj.__code__.co_name,
                "firstlineno": obj.__code__.co_firstlineno,
                "lnotab": obj.__code__.co_lnotab.decode('unicode-escape'),
                "globals": {},
            }
            return JSON.format(
                type=type(obj),
                id=id(obj),
                items=Formatter().to_json(func_code, self.dumps),
            )

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

        if s.startswith('"'):
            return s.strip('"')
        elif s in self._KEYWORDS.values():
            return self._get_key(s, self._KEYWORDS)
        elif self._to_number(s) is not None:
            return self._to_number(s)

        obj_type = self._obj_type_from_template(s, r"<class '(\w\S+)'>_")
        obj_data = self._load_from_dictlike_str(s)

        if issubclass(obj_type, dict):
            return obj_data
        elif issubclass(obj_type, Iterable):
            return obj_type(obj_data.values())
        elif issubclass(obj_type, FunctionType):
            obj_data['code'] = bytes(obj_data['code'].encode())
            obj_data['lnotab'] = bytes(obj_data['lnotab'].encode())

            return obj_type(
                code=CodeType(*list(obj_data.values())[:-1]),
                globals=obj_data['globals']
            )
