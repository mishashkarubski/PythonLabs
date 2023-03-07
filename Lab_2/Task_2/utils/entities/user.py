"""This module defines the CLI user class. Users can
mani"""
from string import punctuation
from re import Pattern
from typing import NoReturn

from .storage import Storage
from ..constants.messages import LOAD_QUESTION, INVALID_RESPONSE


class User:
    """Represents a CLI user. Can operate the attached container, thus

    has access to its every method. Besides, can switch to other users."""

    def __init__(self, username: str | None = None):
        self._username = username
        self._container = Storage()
        self._container.load(username)

    @classmethod
    def verify_username(cls, username: str) -> bool:
        """Checks if username consists only of latin letters and numbers

        :param username: username to verify;
        :return: True, if username is correct; False, otherwise.
        """
        return bool(sum(char in username for char in punctuation))

    @property
    def username(self) -> str | None:
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

    def add_keys(self, *keys: tuple[str]) -> NoReturn:
        """Adds keys to container

        :param keys: tuple of keys to add to container."""
        self.container.add(*keys)

    def remove_key(self, key: tuple[str]) -> NoReturn:
        """Removes a single key from container

        :param key: single key tuple."""
        self.container.remove(*key)

    def list_data(self) -> NoReturn:
        """Prints data in user-friendly format."""
        print(f"[{', '.join(self.container.list())}]")

    def find_key(self, key: tuple[str]) -> NoReturn:
        """Prints the output of Storage's find method.

        :param key: single key tuple."""
        print(self.container.find(*key))

    def grep_keys(self, regex: tuple[str | bytes | Pattern[bytes]]) -> NoReturn:
        """Prints the output of Storage's find method.

        :param regex: single regex tuple."""
        print(self.container.grep(*regex))

    def save_data(self) -> NoReturn:
        """Saves data to the file with user's name as a filename."""
        self.container.save(self.username)

    def load_data(self) -> NoReturn:
        """Loads data from the file with user's name as a filename."""
        self.container.load(self.username)

    def switch(self, new_username: tuple[str]) -> NoReturn:
        """Switches to another user.

        While switching, can load other user's container if needed.
        :param new_username: other user's name to switch on.
        """
        ans: str = input(LOAD_QUESTION.format(new_username[0]))

        if ans == 'y':
            self._container.load(new_username[0], switch=True)
        elif ans != 'n':
            print(INVALID_RESPONSE)

        self.username = new_username[0]
