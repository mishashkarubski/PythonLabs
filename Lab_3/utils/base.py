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
from typing import Any, IO, Hashable, Collection


class Serializer(ABC):
    _JSON_KEYWORDS: dict[None | bool, str] = {
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
        'code': CodeType,
        'cell': CellType,
        'function': FunctionType,
        'lambda': LambdaType,
        'method': MethodType,
        'type': type,
        'module': ModuleType,
        'object': object,
    }

    @classmethod
    def _to_number(cls, s: str) -> int | float | complex | None:
        for num_type in (int, float, complex):
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

    def get_items(self, obj) -> dict[str, Any]:
        """

        :param obj:
        :return:
        """
        if isinstance(obj, dict):
            return obj

        elif isinstance(obj, Collection):
            return dict(enumerate(obj))

        elif isinstance(obj, CodeType):
            return {
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
            }

        elif isinstance(obj, FunctionType):
            if obj.__closure__ and "__class__" in obj.__code__.co_freevars:
                closure = ([... for _ in obj.__closure__])
            else:
                closure = obj.__closure__

            return {
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
                    for k in (
                        set(
                            k for k, v in obj.__globals__.items()
                            if isinstance(v, ModuleType)
                        ) |
                        set(obj.__globals__) &
                        set(obj.__code__.co_names) -
                        {obj.__name__}
                    )
                },
                "closure": closure,
                "qualname": obj.__qualname__
            }

        elif isinstance(obj, MethodType):
            return {
                "__func__": obj.__func__,
                "__self__": obj.__self__
            }

        elif issubclass(type(obj), type):
            return {
                'name': obj.__name__,
                'mro': tuple(obj.mro()[1:-1]),
                'attrs': {
                    k: v for k, v in obj.__dict__.items()
                    if k not in self._NOT_SERIALIZABLE
                }
            }

        elif issubclass(type(obj), ModuleType):
            return {'name': obj.__name__}

        else:
            return {
                'class': obj.__class__,
                'attrs': {
                    k: v for k, v in obj.__dict__.items()
                    if k not in self._NOT_SERIALIZABLE
                }
            }

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
