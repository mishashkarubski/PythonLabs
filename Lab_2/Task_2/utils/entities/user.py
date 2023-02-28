from string import punctuation
from typing import (
    Optional,
    NoReturn,
    Tuple,
    Pattern
)

from .storage import Storage
from ..constants.messages import LOAD_QUESTION, INVALID_RESPONSE


class User:
    """Represents CLI user. Can operate the attached container, thus

    has access to its every method. Besides, can switch to other users."""

    def __init__(self, username: Optional[str] = None):
        self._username = username
        self._container = Storage()
        self._container.load(username)

    @classmethod
    def verify_username(cls, username: str) -> bool:
        return bool(sum(char in username for char in punctuation))

    @property
    def username(self) -> Optional[str]:
        """Getter of attribute __username"""
        return self._username

    @username.setter
    def username(self, new_username: str) -> NoReturn:
        """Setter of attribute __username"""
        self._username = new_username

    @property
    def container(self) -> Storage:
        """Getter of attribute __container"""
        return self._container

    def add_keys(self, keys: Tuple[str]) -> NoReturn:
        """Adds keys to self.container

        Arguments:
        1. keys – tuple of keys to add to container."""
        self.container.add(keys)

    def remove_key(self, key: Tuple[str]) -> NoReturn:
        """Removes a single key from self.container

        Arguments:
        1. key: key to remove from self.container"""
        self.container.remove(key[0])

    def list_data(self) -> NoReturn:
        """Prints data in user-friendly format."""
        print(f"[{', '.join(self.container.list())}]")

    def find_key(self, key: Tuple[str]) -> NoReturn:
        """Prints the output of Storage's find method.

        Arguments:
        1. key: tuple consisting of one key"""
        print(self.container.find(key[0]))

    def grep_keys(self, regex: Tuple[str | Pattern | Pattern[bytes]]) -> NoReturn:
        """Prints the output of Storage's find method."""

        regex = regex[0]
        print(self.container.grep(regex))

    def save_data(self) -> NoReturn:
        """Saves data to the file with user's name as a filename."""
        self.container.save(self.username)

    def load_data(self) -> NoReturn:
        """Loads data from the file with user's name as a filename."""
        self.container.load(self.username)

    def switch(self, new_username: Tuple[str]):
        """Switches to another user.

        While switching, can load other user's container if needed.
        Arguments:
        1. new_username: tuple of single string"""
        ans = input(LOAD_QUESTION.format(new_username[0]))

        if ans in ['y', 'n']:
            self._container.load(
                new_username[0] if ans == 'y' else '',
                switch=(ans == 'y')
            )
            self.username = new_username[0]
        else:
            print(INVALID_RESPONSE)
            return
