import re
from abc import ABC, abstractmethod
from types import (
    NoneType,
    FunctionType,
    LambdaType,
    MethodType,
    CodeType,
    CellType,
    ModuleType
)
from typing import Any, IO, Hashable


class Serializer(ABC):
    _NUMERICS: tuple[type, type, type] = (int, float, complex)
    _KEYWORDS: dict[None | bool, str] = {
        None: 'null',
        True: 'true',
        False: 'false'
    }
    _NOT_SERIALIZABLE: set[str] = {
        '__weakref__',
        '__subclasshook__',
        '__dict__'
    }
    _TYPE_MAPPING = {
        'int': int,
        'float': float,
        'complex': complex,
        'str': str,
        'bool': bool,
        'NoneType': NoneType,
        'ellipsis': Ellipsis,
        'bytes': bytes,
        'list': list,
        'tuple': tuple,
        'set': set,
        'dict': dict,
        'CodeType': CodeType,
        'CellType': CellType,
        'FunctionType': FunctionType,
        'LambdaType': LambdaType,
        'MethodType': MethodType,
        'type': type,
        'ModuleType': ModuleType,
        'object': object,
    }

    @classmethod
    def _to_number(cls, s: str) -> int | float | complex | None:
        for num_type in cls._NUMERICS:
            try:
                return num_type(s)
            except (ValueError, TypeError):
                pass

    @staticmethod
    def _get_key(value: Hashable, obj: dict):
        return [key for key in obj if obj[key] == value][0]

    @classmethod
    def _obj_type_from_template(cls, s: str, pattern: str) -> type:
        if not re.search(pattern, s):
            return NoneType

        return cls._TYPE_MAPPING[re.search(pattern, s).group(1)]

    def dump(self, obj: Any, fp: IO[str]) -> None:
        """Dumps an object to .json file.

        :param obj: object to dump.
        :param fp: json file object.
        """
        fp.write(self.dumps(obj))

    def load(self, fp: IO[str]):
        """Loads an object from .json file.

        :param fp: json file object to extract object from.
        :return: deserialized Python object.
        """
        return self.loads(fp.read())

    @abstractmethod
    def dumps(self, obj) -> str:
        """Dumps an object to a string and returns the string.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        raise NotImplementedError

    @abstractmethod
    def loads(self, s):
        """Loads an object from a string and returns it.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        raise NotImplementedError
