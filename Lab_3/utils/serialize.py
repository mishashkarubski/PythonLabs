"""Serialization of Lab_3"""
import re
from abc import ABC, abstractmethod
from types import NoneType, FunctionType, CodeType
from typing import Callable, Any, IO

from .templates.json_template import FUNCTION_TEMPLATE


class Serializer(ABC):
    _BASE_TYPES = [int, float, complex, bytes, str, NoneType, bool]
    _KEYWORDS = {'None': None, 'True': True, 'False': False}

    def __init__(self):
        pass

    @abstractmethod
    def dump(self, obj: Any, fp: IO[str]) -> None:
        """Dumps an object to IO stream supporting .write() (e.g. a file).

        :param obj: object to dump.
        :param fp: input/output stream to dump object to.
        """
        pass

    @abstractmethod
    def dumps(self, obj):
        """Dumps an object to a string and returns the string.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        pass

    @abstractmethod
    def load(self, fp):
        """Loads an object from IO stream supporting .read() (e.g. a file).

        :param fp: json file object to extract object from.
        :return: deserialized Python object.
        """
        pass

    @abstractmethod
    def loads(self, s):
        """Loads an object from a string and returns it.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        pass


class JSONSerializer(Serializer):
    """JSON serializer class."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse_template(template: str) -> dict[str, str]:
        return dict(re.findall(r'(\w+):\s?([^,{]*)', template)[1:])

    @classmethod
    def _apply_base_types(cls, s: str) -> Any:
        if s in cls._KEYWORDS:
            return cls._KEYWORDS[s]

        for base_type in cls._BASE_TYPES:
            try:
                return base_type(s)
            except (ValueError, TypeError):
                pass

        return None

    @classmethod
    def _typify(cls, data: dict[str, str]) -> dict[str, Any]:
        mid_data = {
            key: cls._apply_base_types(value)
            for key, value in data.items()
        }

        for key, value in data.items():
            if " " in value:
                mid_data[key] = tuple(map(
                    lambda x: cls._apply_base_types(x),
                    value.split()
                ))
            if key == "names":
                mid_data[key] = tuple(value)
            if key == "codestring" or key == "lnotab":
                mid_data[key] = value.encode()

        return mid_data

    def dump(self, obj: Any, fp: IO[str]) -> None:
        """Dumps an object to .json file.

        :param obj: object to dump.
        :param fp: json file object.
        """
        if type(obj) in self._BASE_TYPES:
            if type(obj) == str:
                fp.write(f'"{obj}"')
            else:
                fp.write(str(obj))

    def dumps(self, obj: Any) -> str:
        """Dumps an object to a string and returns the string.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        if type(obj) in self._BASE_TYPES:
            return f"{repr(obj)}"

        if isinstance(obj, FunctionType):
            return FUNCTION_TEMPLATE.format(
                name=obj.__code__.co_name,
                argcount=obj.__code__.co_argcount,
                posonlyargcount=obj.__code__.co_posonlyargcount,
                kwonlyargcount=obj.__code__.co_kwonlyargcount,
                nlocals=obj.__code__.co_nlocals,
                stacksize=obj.__code__.co_stacksize,
                flags=obj.__code__.co_flags,
                code=obj.__code__.co_code.decode('unicode-escape'),
                consts=' '.join(map(str, obj.__code__.co_consts)),
                names=' '.join(obj.__code__.co_names),
                varnames=' '.join(obj.__code__.co_varnames),
                filename=obj.__code__.co_filename,
                firstlineno=obj.__code__.co_firstlineno,
                lnotab=obj.__code__.co_lnotab.decode('unicode-escape'),
            )

    def load(self, fp: IO[str]):
        """Loads an object from .json file.

        :param fp: json file object to extract object from.
        :return: deserialized Python object.
        """
        fp_content: str = fp.read()
        return self.loads(fp_content)

    def loads(self, s: str) -> Any:
        """Loads an object from a string and returns it.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if s.startswith("'") or s.startswith('"'):
            return s.strip("'\"")

        return FunctionType(
            code=CodeType(*self._typify(self._parse_template(s)).values()),
            globals=globals()
        )
