from .storage import Storage
from typing import Optional, NoReturn, Tuple, Pattern
from ..constants.messages import LOAD_QUESTION


class User:
    def __init__(self, username: Optional[str] = None):
        self.__username = username
        self.__container = Storage()
        self.__container.load(username)

    @property
    def username(self) -> Optional[str]:
        return self.__username

    @username.setter
    def username(self, new_username: str) -> NoReturn:
        self.__username = new_username

    @property
    def container(self) -> Storage:
        return self.__container

    def add_keys(self, keys: Tuple[str]) -> NoReturn:
        self.container.add(keys)

    def remove_key(self, key: Tuple[str]) -> NoReturn:
        self.container.remove(key[0])

    def list_data(self) -> NoReturn:
        print(f"[{', '.join(self.container.list())}]")

    def find_key(self, key: Tuple[str]) -> NoReturn:
        print(self.container.find(key[0]))

    def grep_keys(self, regex: Tuple[str | Pattern | Pattern[bytes]]) -> NoReturn:
        regex = regex[0]
        print(self.container.grep(regex))

    def save_data(self) -> NoReturn:
        self.container.save(self.username)

    def load_data(self) -> NoReturn:
        self.container.load(self.username)

    def switch(self, new_username: Tuple[str]):
        self.username = new_username[0]
        ans = input(LOAD_QUESTION.format(self.username))
        
        if ans in ['y', 'n']:
            self.__container.load(
                new_username[0] if ans == 'y' else '',
                switch=(ans == 'y')
            )

