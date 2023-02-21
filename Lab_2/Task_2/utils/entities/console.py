from .user import User
from ..constants.messages import \
    START_MESSAGE, \
    CLI_MESSAGE, \
    INVALID_COMM_MESSAGE, \
    INVALID_PARAM_MESSAGE, \
    END_MESSAGE
from ..constants.types import Command
from typing import NoReturn, Tuple, Dict, Callable
import inspect


class Console:
    def __init__(self):
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
        return self.__user

    @user.setter
    def user(self, new_username: str) -> NoReturn:
        self.user = User(new_username)

    @property
    def commands(self) -> Dict[str, Callable]:
        return self.__commands

    @staticmethod
    def parse_cmd() -> Tuple[str, Tuple[str]]:
        raw_input = input(CLI_MESSAGE).split(maxsplit=1)

        try:
            return raw_input[0], (
                tuple(''),
                tuple(raw_input[-1].split())
            )[len(raw_input) > 1]
        except IndexError:
            return '', tuple('')

    def run(self, comm: str, args: Tuple[str]) -> NoReturn:
        if comm == '':
            return

        if comm not in self.commands:
            print(INVALID_COMM_MESSAGE)
            return

        func = self.commands[comm]
        func_params = inspect.signature(func).parameters

        if (func_params and not args) or (args and not func_params):
            print(INVALID_PARAM_MESSAGE)
            return

        func(args) if args else func()

    def start_session(self) -> NoReturn:
        print(START_MESSAGE)

        while True:
            try:
                self.run(*self.parse_cmd())
            except KeyboardInterrupt:
                print(END_MESSAGE)
                return
