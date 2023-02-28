"""Flexible container for unique elements.

Can be saved to and loaded from different .dmp files
using pickle as a serialization tool.
"""
import os
import re
import pickle
from typing import (
    NoReturn,
    Pattern,
    Optional,
    Any
)


class Storage:
    """Set-based container for storing unique elements

    Supports following operations:
    add <key> [key, ...] – adds one or more elements to container;
    remove <key> – delete key from container;
    find <key> [key, ...] – checks if the element is presented in the container;
    list – returns all elements of container;
    grep <regex> – check the value in the container by regular expression;
    save/load – saves/loads container to/from file;
    switch – switches to another user.
    """
    __SAVE_FOLDER = os.path.relpath("Lab_2/Task_2/data")

    def __init__(self):
        self.__data = set()

    @property
    def data(self) -> set[str]:
        """Getter of attribute __data"""
        return self.__data

    @data.setter
    def data(self, new_data: set[str]) -> NoReturn:
        """Setter of attribute __data"""
        self.__data = new_data

    @classmethod
    def __verify_path(cls, path: str | os.PathLike | bytes) -> bool:
        """Checks if the given path exists.

        :param path: path to check"""
        return os.path.lexists(path)

    @classmethod
    def pathify(cls, name: str | os.PathLike) -> str:
        """Creates a path by concatenating __SAVE_FOLDER with the given name

        :param name: typically storage owner's name to pathify"""
        return os.path.join(cls.__SAVE_FOLDER, name)

    def add(self, *keys: tuple[str]) -> NoReturn:
        """Adds new keys to the storage.

        :param keys: tuple of strings to add to the storage"""
        self.data.update(*keys)

    def remove(self, key: str) -> NoReturn:
        """Removes key from self.data.

        Throws an error if the key doesn't exit.
        :param: key: string"""
        try:
            self.data.remove(key)
        except KeyError:
            print(f"No such key: {key}. Skipping.")

    def list(self) -> list:
        """Returns list of elements"""
        return list(self.data)

    def find(self, key: str) -> str:
        """Returns key if key is present in self.data.

        Otherwise, returns sting 'No such elements.'
        :param  key: key to find in storage"""
        return key if key in self.data else "No such elements."

    def grep(self, regex: str | Pattern | Pattern[bytes]) -> list:
        """Uses regular expressions to find elements in storage

        :param regex: regex-like object to filter data."""
        try:
            return list(filter(lambda k: re.match(regex, k), self.data))
        except re.error:
            return []

    def load(self, source: str, switch=False) -> NoReturn:
        """Loads data to storage from container with the given path.

        :param source: name of the source file to load data from;
        :param switch: if loading is performed on user switch or not."""
        path: str = self.pathify(f"{source}.dmp")

        if not self.__verify_path(path):
            if switch:
                self.data = set()
            return

        with open(path, 'rb') as load_file:
            try:
                new_data: Any = pickle.load(load_file)
            except pickle.UnpicklingError:
                new_data = set()

            self.data = (self.data | new_data) if not switch else new_data

    def save(self, destination: str) -> NoReturn:
        """Saves data to the file with the given path.

        :param destination: name of the destination file to save data to."""
        path: str = self.pathify(f"{destination}.dmp")

        with open(path, 'wb+') as save_file:
            pickle.dump(self.data, save_file)
