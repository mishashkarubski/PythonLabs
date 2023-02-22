"""Program's CLI class for manipulatig storages & its methods."""
from .user import User
from ..constants.messages import \
    START_MESSAGE, \
    CLI_INPUT, \
    INVALID_COMM_MESSAGE, \
    INVALID_ARG_MESSAGE, \
    END_MESSAGE, \
    SAVE_QUESTION
from ..constants.types import Command
from typing import NoReturn, Tuple, Dict, Callable
import inspect


# TODO #1: Code cleanup & bug fixes
# TODO #2: Refactoring

class Console:
    """Console is a main class of the program.

    It can create, delete, and manipulate users and storages.
    """
    def __init__(self):
        print(START_MESSAGE)
        self.__user = User(input("Username: "))
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
        raw_input = input(CLI_INPUT).split(maxsplit=1)

        try:
            return raw_input[0], (
                tuple(''),
                tuple(raw_input[-1].split())
            )[len(raw_input) > 1]
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

        while True:
            try:
                self.run(*self.parse_cmd())
            except KeyboardInterrupt:
                ans = input(SAVE_QUESTION)
                if ans in ['y', 'n']:
                    self.run('save' if ans == 'y' else '', tuple(''))
                    print(END_MESSAGE)
                    return
