"""Serialization of Lab_3"""
import re
from abc import ABC, abstractmethod
from types import NoneType, FunctionType, CodeType
from typing import Callable, Any, IO

from .templates.json_template import FUNCTION_TEMPLATE


class Serializer(ABC):
    _BASE_TYPES = [int, float, complex, bytes, str, NoneType, bool]

    def __init__(self):
        pass

    @staticmethod
    def _apply_base_types(types, s: str) -> Any:
        results = []
        for t in types:
            try:
                results.append(t(s.strip('()')))
            except (ValueError, TypeError):
                results.append(None)

        return tuple(filter(lambda x: x is not None, results))[0]

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
    def _parse_dictlike(cls: str) -> dict[str, str]:
        function_meta = re.findall(
            r'(\w+):\s?(.*)',
            cls.replace(",", "").replace("{", "")
        )
        return dict(function_meta[1:])

    @classmethod
    def _process_dict(cls, data: dict[str, str]) -> dict[str, Any]:
        mid_data = {
            key: cls._apply_base_types(cls._BASE_TYPES, value)
            for key, value in data.items()
        }

        for k, v in data.items():
            if " " in v:
                mid_data[k] = tuple(map(
                    lambda x: cls._apply_base_types(cls._BASE_TYPES, x),
                    v.split()
                ))
                if k == "consts":
                    mid_data[k] = (None, *list(map(
                        lambda x: cls._apply_base_types(cls._BASE_TYPES, x),
                        v.split()
                    ))[1:])
            if k == "names":
                mid_data[k] = tuple()
            if "b'" in v:
                print()
                print(v)
                print()
                mid_data[k] = v.encode('unicode-escape').decode('unicode-escape').encode()
                print(mid_data[k])

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
            code_info = obj.__code__
            return FUNCTION_TEMPLATE.format(
                name=code_info.co_name,
                argcount=code_info.co_argcount,
                posonlyargcount=code_info.co_posonlyargcount,
                kwonlyargcount=code_info.co_kwonlyargcount,
                nlocals=code_info.co_nlocals,
                stacksize=code_info.co_stacksize,
                flags=code_info.co_flags,
                code=code_info.co_code,
                consts=code_info.co_consts,
                names=code_info.co_names,
                varnames=' '.join(code_info.co_varnames),
                filename=code_info.co_filename,
                firstlineno=code_info.co_firstlineno,
                lnotab=code_info.co_lnotab,
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
            code=CodeType(*self._process_dict(
                self._parse_dictlike(s)
            ).values()),
            globals=globals()
        )
