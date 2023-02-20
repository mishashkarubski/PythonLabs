"""Set-based containter for storing unique elements

Supports following operations:
add <key> [key, ...] – adds one or more elements to container;
remove <key> – delete key from container;
find <key> [key, ...] – checks if the element is presented in the container;
list – returns all elements of container;
grep <regex> – check the value in the container by regular expression
save/load – save/load container to/from file;
"""
import re


class Storage:
    def __init__(self):
        self.__data = set()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_data):
        self.__data = new_data

    def add(self, *keys):
        self.data.update(keys)

    def remove(self, key):
        self.data.remove(key)

    def list(self):
        return list(self.data)

    def find(self, key):
        return key in self.data

    def grep(self, regex):
        return list(filter(lambda k: re.match(regex, k), self.data))

    def load(self):
        pass

    def save(self):
        pass
