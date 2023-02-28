"""Program's CLI class for manipulating storages."""
import inspect
import string
import random
from typing import (
    NoReturn,
    Tuple,
    Dict,
    Callable
)

from .user import User
from ..constants.types import Command
from ..constants.messages import (
    START_MESSAGE,
    CLI_INPUT,
    INVALID_COMM_MESSAGE,
    INVALID_ARG_MESSAGE,
    END_MESSAGE,
    USERNAME_REQUEST,
    SAVE_QUESTION,
    INVALID_RESPONSE
)


class Console:
    """Console is a main class of the program.

    It can create, delete, and manipulate users and storages.
    """

    def __init__(self):
        print(START_MESSAGE)

        self.__user = None
        self.__stop_early = False

        while not self.__user or self.__user.verify_username(self.__user.username):
            try:
                self.__user = User(input(USERNAME_REQUEST))
            except KeyboardInterrupt:
                self.__stop_early = True
                self.__user = User(random.choices(population=string.ascii_letters, k=10))

        self.__commands = {
            Command.add.value: self.__user.add_keys,
            Command.remove.value: self.__user.remove_key,
            Command.find.value: self.__user.find_key,
            Command.list.value: self.__user.list_data,
            Command.grep.value: self.__user.grep_keys,
            Command.save.value: self.__user.save_data,
            Command.load.value: self.__user.load_data,
            Command.switch.value: self.__user.switch
        }

    @property
    def user(self) -> User:
        """Getter of attribute __user"""
        return self.__user

    @user.setter
    def user(self, new_username: str) -> NoReturn:
        """Setter of attribute __user"""
        self.user = User(new_username)

    @property
    def commands(self) -> Dict[str, Callable]:
        """Getter of attribute __commands"""
        return self.__commands

    @staticmethod
    def parse_cmd() -> Tuple[str, Tuple[str]]:
        """Parses command line input and returns tuple

        containing command and its arguments.
        """
        raw_input = input(CLI_INPUT).split(maxsplit=1)

        try:
            return raw_input[0], (
                tuple(raw_input[-1].split()) if len(raw_input) > 1
                else tuple('')
            )
        except IndexError:
            return '', tuple('')

    def run(self, comm: str, args: Tuple[str]) -> NoReturn:
        """Runs the given command with the given arguments.

        If something wrong, displays error message. Args:
        1. comm: string
        2. args: tuple of strings
        """
        if comm == '':
            return

        if comm not in self.commands:
            print(INVALID_COMM_MESSAGE.format(comm))
            return

        func = self.commands[comm]
        func_params = inspect.signature(func).parameters

        if (func_params and not args) or (args and not func_params):
            print(INVALID_ARG_MESSAGE.format(", ".join(args)))
            return

        func(args) if args else func()

    def start_session(self) -> NoReturn:
        """Starts CLI session and turns on interactive mode"""

        if self.__stop_early:
            print(END_MESSAGE)
            return

        while True:
            try:
                self.run(*self.parse_cmd())
            except KeyboardInterrupt:
                self.stop_session()
                return

    def stop_session(self):
        """A wire..."""

        try:
            ans = input(SAVE_QUESTION)
        except KeyboardInterrupt:
            return

        if not ans or ans not in ['y', 'n']:
            print(INVALID_RESPONSE)
            return

        self.run('save' if ans == 'y' else '', tuple(''))
        print(END_MESSAGE)
