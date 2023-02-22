"""Program's CLI class for manipulatig storages & its methods."""
import inspect
from typing import NoReturn, Tuple, Dict, Callable

from .user import User
from ..constants.types import Command
from ..constants.messages import MESSAGES as MSG


# TODO #1: Code cleanup & bug fixes
# TODO #2: Refactoring

class Console:
    """Console is a main class of the program.

    It can create, delete, and manipulate users and storages.
    """

    def __init__(self):
        print(MSG['START_MESSAGE'])

        self.__user = None

        while not self.__user:
            try:
                self.__user = User(input("Username: "))
            except KeyboardInterrupt:
                print()

        self.__commands = {
            Command.add.value: self.__user.add_keys,
            Command.remove.value: self.__user.remove_key,
            Command.find.value: self.user.find_key,
            Command.list.value: self.user.list_data,
            Command.grep.value: self.user.grep_keys,
            Command.save.value: self.user.save_data,
            Command.load.value: self.user.load_data,
            Command.switch.value: self.user.switch
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
        raw_input = input(MSG['CLI_INPUT']).split(maxsplit=1)

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
            print(MSG['INVALID_COMM_MESSAGE'].format(comm))
            return

        func = self.commands[comm]
        func_params = inspect.signature(func).parameters

        if (func_params and not args) or (args and not func_params):
            print(MSG['INVALID_ARG_MESSAGE'].format(", ".join(args)))
            return

        func(args) if args else func()

    def start_session(self) -> NoReturn:
        """Starts CLI session and turns on interactive mode"""

        while True:
            try:
                self.run(*self.parse_cmd())
            except KeyboardInterrupt:
                self.stop_session()
                return

    def stop_session(self):
        ans = input(MSG['SAVE_QUESTION'])

        if ans not in ['y', 'n']:
            print(MSG['INVALID_COMM_MESSAGE'])
            return

        self.run('save' if ans == 'y' else '', tuple(''))
        print(MSG['END_MESSAGE'])
