"""Serialization of Lab_3"""
import types
from abc import ABC, abstractmethod
from types import NoneType
from typing import Callable, Any, IO


class Serializer(ABC):
    _BASE_TYPES = [int, float, complex, bool, str, NoneType]

    def __init__(self):
        pass

    @abstractmethod
    def dump(self, obj, fp):
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
            return None

        if s.startswith("'") or s.startswith('"'):
            return s.strip("'\"")

        for t in self._BASE_TYPES:
            try:
                return t(s) if t != bool else (True, False)[s == "False"]
            except ValueError:
                pass
