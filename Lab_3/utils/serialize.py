"""Serialization of Lab_3"""
import re
from abc import ABC, abstractmethod
from types import (
    FunctionType,
    CodeType,
    NoneType,
    LambdaType,
    MethodType
)
from typing import (
    Any,
    IO,
    Hashable,
    Iterable
)

from .templates.json_templates import (
    ITERABLE,
    CALLABLE,
    DICTIONARY
)


# TODO *1: Add dictionary serialization support (+ tests).
# TODO *2: Add nested data structures serialization support (+ tests).
# TODO *3: Add globals and closures support for function serialization (+ tests).
# TODO *4: Add method serialization support (+ tests).
# TODO *5: Add class & object serialization support (+ tests).
# TODO *6: Add scope serialization support (+ tests).
# TODO *7: Add library serialization support (+ tests).

# TODO *8: Add XAML serialization templates (+ tests).


class Formatter:
    def shift(self, s, indent):
        return "\t" * indent + s


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
    def _key_by_value(value: Hashable, data: dict):
        return [key for key in data if data[key] == value][0]

    @staticmethod
    def _obj_type_from_template(s: str) -> type:
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

    def _typify_list(self, lst: list[str]):
        temp_lst = lst.copy()

        for index, item in enumerate(temp_lst):
            if self._numeric(item) is not None:
                temp_lst[index] = self._numeric(item)

            elif item in self._KEYWORDS.values():
                temp_lst[index] = self._key_by_value(item, self._KEYWORDS)

            else:
                temp_lst[index] = self.loads(item)

        return temp_lst

    def _typify_dict(self, data: dict[str, str]) -> dict[Any, Any] | None:
        if not data:
            return

        temp_data: dict[str, Any] = data.copy()

        for key, value in temp_data.items():
            if type(value) == str and value.startswith('"'):
                temp_data[key] = value.strip('"')

            if self._numeric(value) is not None:
                temp_data[key] = self._numeric(value)

            if value in self._KEYWORDS.values():
                temp_data[key] = self._key_by_value(value, self._KEYWORDS)

            if key == "codestring" or key == "lnotab":
                temp_data[key] = value.encode()

            if key in ("items", "consts", "names", "varnames"):
                lst, temp_item, quotes = [], "", False

                for ind, char in enumerate(value):
                    if char == " " and not quotes:
                        lst.append(temp_item)
                        temp_item = ""

                    elif ind == len(value) - 1 and temp_item.strip():
                        temp_item += char
                        lst.append(temp_item.strip())

                    elif char == '"':
                        quotes = not quotes

                    temp_item += char

                temp_data[key] = tuple(self._typify_list(lst=lst)) if value else ()

        return temp_data

    def _template_to_dict(self, template: str):
        new_index: int = 0
        obj: dict[Any, Any] = {}
        lines: list[str] = template.split("\n")

        for index in range(len(lines)):
            if new_index > index:
                index = new_index

            if not re.search(r'(.+)\s*:\s*(.+)', lines[index]):
                continue

            line_info = re.search(r'\s*(.+):\s*(.*)', lines[index])
            key, value = line_info.group(1), line_info.group(2).strip(", ")

            if value != "{":
                obj[self.loads(key)] = value

            elif value == "{" and "class" not in key:
                brackets = 1
                new_index = index
                complex_value = ""

                while brackets:
                    new_index += 1

                    complex_value += lines[new_index] + "\n"

                    brackets += "{" in lines[new_index]
                    brackets -= "}" in lines[new_index]

                obj[self.loads(key)] = self.loads(complex_value[:-4])

        return obj

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
        if type(obj) == str:
            return f'"{obj}"'

        if type(obj) in self._NUMERICS:
            return str(obj)

        if isinstance(obj, dict):
            items_repr = ""

            for k, v in obj.items():
                if type(v) in [*self._NUMERICS, str, bool, NoneType]:
                    items_repr += f"\t{self.dumps(k)}: {self.dumps(v)},\n"
                    continue

                dumped_value = self.dumps(v).split("\n")
                items_repr += f"\t{self.dumps(k)}: {{\n"

                for line in dumped_value[1:]:
                    items_repr += f"{Formatter().shift(line, 1)}\n"

            return DICTIONARY.format(
                id=id(obj),
                items=items_repr,
            )

        if isinstance(obj, Iterable):
            return ITERABLE.format(
                type=type(obj),
                id=id(obj),
                items=' '.join(list(map(self.dumps, obj)))
            )

        if obj in self._KEYWORDS:
            return self._KEYWORDS[obj]

        if isinstance(obj, FunctionType):
            return CALLABLE.format(
                type=type(obj),
                id=id(obj),
                argcount=self.dumps(obj.__code__.co_argcount),
                posonlyargcount=self.dumps(obj.__code__.co_posonlyargcount),
                kwonlyargcount=self.dumps(obj.__code__.co_kwonlyargcount),
                nlocals=self.dumps(obj.__code__.co_nlocals),
                stacksize=self.dumps(obj.__code__.co_stacksize),
                flags=self.dumps(obj.__code__.co_flags),
                code=self.dumps(obj.__code__.co_code.decode('unicode-escape')),
                consts=str(obj.__code__.co_consts),  # C функциями траблы
                names=self.dumps(obj.__code__.co_names),
                varnames=self.dumps(obj.__code__.co_varnames),
                filename=self.dumps(obj.__code__.co_filename),
                name=self.dumps(obj.__code__.co_name),
                firstlineno=self.dumps(obj.__code__.co_firstlineno),
                lnotab=self.dumps(obj.__code__.co_lnotab.decode('unicode-escape')),
                globals=self.dumps(obj.__globals__)
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
        if not len(s):  # Check if there is a string. Return None if not.
            return

        # String check
        if s.startswith('"'):
            return s.strip('"')

        # Gotta check mutable types first, bc of _KEYWORDS (draft)
        if issubclass(self._obj_type_from_template(s), dict):
            return self._typify_dict(self._template_to_dict(s))

        # Same here
        if issubclass(self._obj_type_from_template(s), Iterable):
            return self._obj_type_from_template(s)(
                self._typify_dict(self._template_to_dict(s))["items"]
            )

        # Then bools and NoneType
        if s in self._KEYWORDS.values():
            return self._key_by_value(s, self._KEYWORDS)

        # Numbers (int, float, complex)
        if self._numeric(s) is not None:
            return self._numeric(s)

        # Functions and lambdas
        if issubclass(self._obj_type_from_template(s), FunctionType):
            func_code: list = list(self._typify_dict(self._template_to_dict(s)).values())

            return self._obj_type_from_template(s)(
                code=CodeType(*func_code),
                globals=func_code[-1],
            )


if __name__ == '__main__':
    from Lab_3 import amoga

    amoga(1, 2)
    json_ser = JSONSerializer()
    # json_ser.loads(json_ser.dumps({1: 2, 2: 3, 3: 4}))
    # print(globals())
    a = {
        1: 2,
        "3": [4, -1, "aboba {([sus])} imposter"],
        5: {
            6: '7',
            8: {
                9: None,
                'None': (True, False)
            },
        }
    }
    print(a == json_ser.loads(json_ser.dumps(a)))
    # print(json_ser.dumps(lambda x: 8 * x**7))
    # print(json_ser.dumps(amoga))
    # print(json_ser.loads(json_ser.dumps(amoga)))
