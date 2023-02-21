import re

from .storage import Storage
from typing import Optional, NoReturn, Tuple


class User:
    def __init__(self, username: Optional[str] = None):
        self.__username = username
        self.__container = Storage()

    @property
    def username(self) -> Optional[str]:
        return self.__username

    @username.setter
    def username(self, new_username: str) -> NoReturn:
        self.username = new_username

    @property
    def container(self) -> Storage:
        return self.__container

    def add_keys(self, keys: Tuple[str]) -> NoReturn:
        self.container.add(keys)

    def remove_key(self, key: Tuple[str]) -> NoReturn:
        self.container.remove(str(key))

    def list_data(self) -> NoReturn:
        print(self.container.list())

    def find_key(self, key: Tuple[str]) -> NoReturn:
        print(self.container.find(str(key)))

    def grep_keys(self, regex) -> NoReturn:
        print(self.container.grep(regex))

    def save_data(self) -> NoReturn:
        self.container.save(self.username)

    def load_data(self) -> NoReturn:
        self.container.load(self.username)

    def switch(self, new_username: str):
        self.username = new_username
        self.container.load(new_username)
