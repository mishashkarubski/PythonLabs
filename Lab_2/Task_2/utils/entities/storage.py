"""Set-based containter for storing unique elements

Supports following operations:
add <key> [key, ...] – adds one or more elements to container;
remove <key> – delete key from container;
find <key> [key, ...] – checks if the element is presented in the container;
list – returns all elements of container;
grep <regex> – check the value in the container by regular expression;
save/load – saves/loads container to/from file;
"""
import os
import re
import pickle


class Storage:
    __SAVE_FOLDER = \
        '/Users/mishashkarubski/PycharmProjects' + \
        '/PythonLabs/Lab_2/Task_2/data/'

    def __init__(self):
        self.__data = set()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_data):
        self.__data = new_data

    @classmethod
    def __verify_path(cls, path: str | os.PathLike):
        return os.path.lexists(path)

    @classmethod
    def pathify(cls, name):
        return os.path.join(cls.__SAVE_FOLDER, name)

    def add(self, *keys):
        self.data.update(*keys)

    def remove(self, key):
        self.data.remove(key)

    def list(self):
        return list(self.data)

    def find(self, key):
        return key in self.data

    def grep(self, regex):
        return list(filter(lambda k: re.match(regex, k), self.data))

    def load(self, source):
        path = self.pathify(f"{source}.dmp")

        if not self.__verify_path(path):
            return
        with open(path, 'rb') as load_file:
            self.data |= pickle.load(load_file)

    def save(self, destination):
        path = self.pathify(f"{destination}.dmp")

        with open(path, 'wb+') as save_file:
            pickle.dump(self.data, save_file)
