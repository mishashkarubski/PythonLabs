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
    _NUMERICS = [int, float, complex]
    _KEYWORDS = {None: 'null', True: 'true', False: 'false'}
    _NOT_SERIALIZABLE = {'__weakref__', '__subclasshook__', '__dict__'}

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

    @staticmethod
    def _obj_type_from_template(s: str, pattern: str) -> type:
        if not re.search(pattern, s):
            return NoneType

        obj_type = re.search(pattern, s).group(1)

        if not obj_type:
            return NoneType
        if obj_type == 'bytes':
            return bytes
        if obj_type == 'list':
            return list
        elif obj_type == 'tuple':
            return tuple
        elif obj_type == 'set':
            return set
        elif obj_type == 'dict':
            return dict
        elif obj_type == 'code':
            return CodeType
        elif obj_type == 'cell':
            return CellType
        elif obj_type == 'function':
            return FunctionType
        elif obj_type == 'lambda':
            return LambdaType
        elif obj_type == 'method':
            return MethodType
        elif obj_type == 'type':
            return type
        elif obj_type == 'module':
            return ModuleType
        elif obj_type == 'object':
            return object

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
    def dumps(self, obj):
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
