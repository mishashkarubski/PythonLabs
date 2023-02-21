from .user import User
from ..constants.messages import \
    WELCOME_MESSAGE, \
    CLI_MESSAGE, \
    INVALID_COMMAND_MESSAGE
from ..constants.types import Command
from typing import List, NoReturn, Tuple, Optional


class Console:
    def __init__(self):
        self.__user = User(input("Username: "))
        self.__commands = {
            Command.add.value: self.__user.add_keys,
            Command.remove.value: self.__user.remove_key,
            Command.find.value: self.__user.find_key,
            Command.list.value: self.__user.list_data,
            Command.grep.value: self.__user.grep_keys,
            Command.save.value: self.__user.save_data,
            Command.load.value: self.__user.load_data,
        }

    @property
    def user(self) -> User:
        return self.__user

    @user.setter
    def user(self, new_username: str) -> NoReturn:
        self.user = User(new_username)

    @staticmethod
    def parse_cmd() -> Tuple[str, Tuple[str]]:
        raw_input = input(CLI_MESSAGE).split(maxsplit=1)

        try:
            result = raw_input[0], (
                '',
                tuple(raw_input[-1].split())
            )[len(raw_input) > 1]
        except IndexError:
            result = '', tuple('')

        return result

    def run(self, comm: str, args: List[str] | str) -> NoReturn:
        if comm in self.__commands:
            self.__commands[comm](args) if args else self.__commands[comm]()
        elif comm != '':
            print(INVALID_COMMAND_MESSAGE)

    def start_session(self) -> NoReturn:
        print(WELCOME_MESSAGE)

        while True:
            comm, args = self.parse_cmd()
            self.run(comm, args)
