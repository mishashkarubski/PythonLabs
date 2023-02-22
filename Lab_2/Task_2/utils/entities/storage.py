"""Flexible container for unique elements.

Can be saved to and loaded from different .dmp files
using pickle as a serialization tool.
"""
import os
import re
import pickle
from typing import Set, List, NoReturn, Tuple, Pattern


class Storage:
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
    __SAVE_FOLDER = os.path.abspath("Lab_2/Task_2/data")

    def __init__(self):
        self.__data = set()

    @property
    def data(self) -> Set[str]:
        """Getter of attribute __data"""
        return self.__data

    @data.setter
    def data(self, new_data: Set[str]) -> NoReturn:
        """Setter of attribute __data"""
        self.__data = new_data

    @classmethod
    def __verify_path(cls, path: str | os.PathLike | bytes) -> bool:
        """Checks if the given path exists."""
        return os.path.lexists(path)

    @classmethod
    def pathify(cls, name: str | os.PathLike) -> bytes:
        """Creates a path by concatenating __SAVE_FOLDER with the given name"""
        return os.path.join(cls.__SAVE_FOLDER, name)

    def add(self, *keys: Tuple[str]) -> NoReturn:
        """Adds new keys to self.data. Arguments:

        1. keys: tuple of strings to remove from self.data"""
        self.data.update(*keys)

    def remove(self, key: str) -> NoReturn:
        """Removes key from self.data.

        Throws an error if the key doesn't exit. Arguments:
        1. key: string"""
        try:
            self.data.remove(key)
        except KeyError:
            print(f"No such key: {key}. Skipping.")

    def list(self) -> List:
        """Returns list of elements"""
        return list(self.data)

    def find(self, key: str) -> str:
        """Returns key if key is present in self.data.

        Otherwise, returns sting 'No such elements.' Arguments:
        1. key: any string"""
        return key if key in self.data else "No such elements."

    def grep(self, regex: str | Pattern | Pattern[bytes]) -> List:
        """Uses regular expressions to find elements in self.data

        Arguments:
        1. regex: regex-like object to filter data"""
        return list(filter(lambda k: re.match(regex, k), self.data))

    def load(self, source: str, switch=False) -> NoReturn:
        """Loads data into self.data from container with the given path.

        Arguments:
        1. source: name of the source file to load data from;
        2. switch: if loading is performed on user switch or not."""
        path = self.pathify(f"{source}.dmp")

        if not self.__verify_path(path):
            if switch:
                self.data = set()
            return

        with open(path, 'rb') as load_file:
            try:
                new_data = pickle.load(load_file)
            except pickle.UnpicklingError:
                new_data = set()

            self.data = (self.data | new_data) if not switch else new_data

    def save(self, destination: str) -> NoReturn:
        """Saves data to the file with the given path.

        Arguments:
        1. destination: name of the source file to save data to;"""
        path = self.pathify(f"{destination}.dmp")

        with open(path, 'wb+') as save_file:
            pickle.dump(self.data, save_file)
