"""Set-based containter for storing unique elements

Supports following operations:
add <key> [key, ...] – adds one or more elements to container;
remove <key> – delete key from container;
find <key> [key, ...] – checks if the element is presented in the container;
list – returns all elements of container;
grep <regex> – check the value in the container by regular expression;
save/load – saves/loads container to/from file;
switch – switches to another user.
"""
import os
import re
import pickle
from typing import Set, List, NoReturn, Tuple, Pattern


class Storage:
    __SAVE_FOLDER = \
        '/Users/mishashkarubski/PycharmProjects' + \
        '/PythonLabs/Lab_2/Task_2/data/'

    def __init__(self):
        self.__data = set()

    @property
    def data(self) -> Set[str]:
        return self.__data

    @data.setter
    def data(self, new_data: Set[str]) -> NoReturn:
        self.__data = new_data

    @classmethod
    def __verify_path(cls, path: str | os.PathLike | bytes) -> bool:
        return os.path.lexists(path)

    @classmethod
    def pathify(cls, name: str | os.PathLike) -> bytes:
        return os.path.join(cls.__SAVE_FOLDER, name)

    def add(self, *keys: Tuple[str]) -> NoReturn:
        self.data.update(*keys)

    def remove(self, key: str) -> NoReturn:
        try:
            self.data.remove(key)
        except KeyError:
            print(f"No such key: {key}. Skipping.")

    def list(self) -> List:
        return list(self.data)

    def find(self, key: str) -> str:
        return key if key in self.data else "No such elements"

    def grep(self, regex: str | Pattern | Pattern[bytes]) -> List:
        return list(filter(lambda k: re.match(regex, k), self.data))

    def load(self, source: str, switch=False) -> NoReturn:
        path = self.pathify(f"{source}.dmp")

        if not self.__verify_path(path):
            if switch:
                self.data = set()
            return

        with open(path, 'rb') as load_file:
            new_data = pickle.load(load_file)
            self.data = (self.data | new_data) if not switch else new_data

    def save(self, destination: str) -> NoReturn:
        path = self.pathify(f"{destination}.dmp")

        with open(path, 'wb+') as save_file:
            pickle.dump(self.data, save_file)
