"""Program's CLI class for manipulating storages."""
import inspect
import string
import random

from typing import (
    NoReturn,
    Callable,
    Optional,
    KeysView
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

    Creates, deletes, and carries out other actions on users and storages.
    """

    def __init__(self):
        print(START_MESSAGE)

        self.__user: Optional[User] = None
        self.__is_interrupted: bool = False

        while not self.__user or self.__user.verify_username(self.__user.username):
            try:
                self.__user = User(input(USERNAME_REQUEST))
            except KeyboardInterrupt:
                self.__is_interrupted = True
                self.__user = User(random.choices(population=string.ascii_letters, k=10))

        self.__commands: dict[str, Callable] = {
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
    def commands(self) -> dict[str, Callable]:
        """Getter of attribute __commands"""
        return self.__commands

    @staticmethod
    def parse_cmd() -> tuple[str, tuple[str]]:
        """Returns a tuple consisting of command and

        its arguments parsed from CLI input."""

        raw_input: list[str] = input(CLI_INPUT).split(maxsplit=1)

        try:
            return (
                raw_input[0],
                ('', raw_input[-1].split())[len(raw_input) > 1]
            )
        except IndexError:
            return '', tuple('')

    def run(self, comm: str, args: tuple[str]) -> NoReturn:
        """Runs the given command with the given arguments.

        If something wrong, displays error message.
        :param comm: command to execute;
        :param args: command's arguments.
        """
        if not comm:
            return

        if comm not in self.commands:
            print(INVALID_COMM_MESSAGE.format(comm))
            return

        func: Callable = self.commands[comm] if comm else lambda x: None
        func_params: KeysView[str] = inspect.signature(func).parameters.keys()

        if len(func_params) != len(args):
            print(INVALID_ARG_MESSAGE.format(", ".join(args)))
            return

        func(args) if args else func()

    def start_session(self) -> NoReturn:
        """Starts CLI session and turns on interactive mode"""

        if self.__is_interrupted:
            print(END_MESSAGE)
            return

        while True:
            try:
                self.run(*self.parse_cmd())
            except KeyboardInterrupt:
                self.stop_session()
                return

    def stop_session(self):
        """Makes necessary preparations before stopping a session."""

        try:
            ans = input(SAVE_QUESTION)
        except KeyboardInterrupt:
            return

        if not ans or ans not in ['y', 'n']:
            print(INVALID_RESPONSE)
            return

        self.run('save' if ans == 'y' else '', tuple(''))
        print(END_MESSAGE)
