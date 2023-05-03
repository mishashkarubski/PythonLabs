from types import (
    NoneType, FunctionType, LambdaType,
    MethodType, CodeType, CellType, ModuleType
)

PRIMITIVE_TYPES: tuple = (int, float, complex, str, bool, NoneType, type(Ellipsis))
TYPE_MAPPING = {
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
