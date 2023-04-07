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
        pass

    @abstractmethod
    def dumps(self, obj):
        pass

    @abstractmethod
    def load(self, fp):
        pass

    @abstractmethod
    def loads(self, s):
        pass


class JSONSerializer(Serializer):
    def __init__(self):
        super().__init__()

    def dump(self, obj: Any, fp: IO[str]):
        if type(obj) in self._BASE_TYPES:
            if type(obj) == str:
                fp.write(f'"{obj}"')
            else:
                fp.write(str(obj))

    def dumps(self, obj: Any) -> str:
        if type(obj) in self._BASE_TYPES:
            return f"{repr(obj)}"

    def load(self, fp: IO[str]):
        fp_content: str = fp.read()
        return self.loads(fp_content)

    def loads(self, s: str) -> Any:
        if not len(s):
            return None

        if s.startswith("'") or s.startswith('"'):
            return s.strip("'\"")

        for t in self._BASE_TYPES:
            try:
                return t(s) if t != bool else (True, False)[s == "False"]
            except ValueError:
                pass
