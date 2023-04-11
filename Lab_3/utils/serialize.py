"""Serialization of Lab_3"""
import re
from abc import ABC, abstractmethod
from types import FunctionType, CodeType, NoneType, LambdaType, MethodType
from typing import Callable, Any, IO, Hashable, Iterable

from .templates.json_template import ITERABLE, CALLABLE


class Serializer(ABC):
    _NUMERICS = [int, float, complex]
    _KEYWORDS = {None: 'null', True: 'true', False: 'false'}

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
    def _template_to_dict(template: str) -> dict[str, str]:
        return dict(re.findall(r'"(\w+)":\s?"([^,{]*)"', template))

    @staticmethod
    def _get_key(value: Hashable, data: dict):
        return [key for key in data if data[key] == value][0]

    @staticmethod
    def _get_obj_type(s: str) -> type:
        obj_type = re.search(r"<class '(\w\S+)'>_", s)

        if not obj_type:
            return NoneType
        if obj_type.group(1) == 'list':
            return list
        elif obj_type.group(1) == 'tuple':
            return tuple
        elif obj_type.group(1) == 'set':
            return set
        elif obj_type.group(1) == 'dict':
            return dict
        elif obj_type.group(1) == 'function':
            return FunctionType
        elif obj_type.group(1) == 'lambda':
            return LambdaType
        elif obj_type.group(1) == 'method':
            return MethodType

    @classmethod
    def _numeric(cls, s: str) -> Any:
        for num_type in cls._NUMERICS:
            try:
                return num_type(s)
            except (ValueError, TypeError):
                pass

    @classmethod
    def _typify_list(cls, lst: list[str]):
        temp_lst = lst.copy()

        for index, item in enumerate(temp_lst):
            if cls._numeric(item) is not None:
                temp_lst[index] = cls._numeric(item)

            elif item in cls._KEYWORDS.values():
                temp_lst[index] = cls._get_key(item, cls._KEYWORDS)

        return temp_lst

    @classmethod
    def _typify_dict(cls, data: dict[str, str]) -> dict[str, Any]:
        temp_data: dict[str, Any] = data.copy()

        for key, value in temp_data.items():
            if cls._numeric(value) is not None:
                temp_data[key] = cls._numeric(value)

            if value in cls._KEYWORDS.values():
                temp_data[key] = cls._get_key(value, cls._KEYWORDS)

            if key == "codestring" or key == "lnotab":
                temp_data[key] = value.encode()

            if key in ("items", "consts", "names", "varnames"):
                temp_data[key] = tuple(cls._typify_list(value.split()))

        return temp_data

    def dump(self, obj: Any, fp: IO[str]) -> None:
        """Dumps an object to .json file.

        :param obj: object to dump.
        :param fp: json file object.
        """
        fp.write(self.dumps(obj))

    def dumps(self, obj: Any) -> str:
        """Dumps an object to a string and returns the string.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        if isinstance(obj, Iterable):
            return ITERABLE.format(
                type=type(obj),
                id=id(obj),
                items=' '.join(map(str, obj))
            )

        if obj in self._KEYWORDS:
            return self._KEYWORDS[obj]

        if type(obj) == str:
            return f'"{obj}"'

        if type(obj) in self._NUMERICS:
            return str(obj)

        if isinstance(obj, FunctionType):
            return CALLABLE.format(
                type=type(obj),
                id=id(obj),
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
                name=obj.__code__.co_name,
                firstlineno=obj.__code__.co_firstlineno,
                lnotab=obj.__code__.co_lnotab.decode('unicode-escape'),
            )

    def load(self, fp: IO[str]):
        """Loads an object from .json file.

        :param fp: json file object to extract object from.
        :return: deserialized Python object.
        """
        return self.loads(fp.read())

    def loads(self, s: str) -> Any:
        """Loads an object from a string and returns it.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if issubclass(self._get_obj_type(s), Iterable):
            return self._get_obj_type(s)(
                self._typify_dict(self._template_to_dict(s))["items"]
            )

        if s in self._KEYWORDS.values():
            return self._get_key(s, self._KEYWORDS)

        if s.startswith('"'):
            return s.strip('"')

        if self._numeric(s) is not None:
            return self._numeric(s)

        if issubclass(self._get_obj_type(s), FunctionType):
            return self._get_obj_type(s)(
                code=CodeType(*self._typify_dict(self._template_to_dict(s)).values()),
                globals=globals()
            )
