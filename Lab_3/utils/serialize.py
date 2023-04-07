"""Serialization of Lab_3"""
from abc import ABC, abstractmethod
from typing import Callable, Any


class Serializer(ABC):
    _BASE_TYPES = [int, float, complex, bool, str]

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

    # noinspection PyUnresolvedReferences
    def dump(self, obj, fp):
        pass

    def dumps(self, obj) -> str:
        if type(obj) in self._BASE_TYPES:
            return f"{repr(obj)}"

    def load(self, fp):
        pass

    def loads(self, s: str) -> Any:
        if s.startswith("'"):
            return s

        for t in self._BASE_TYPES:
            try:
                return t(s)
            except ValueError:
                pass
