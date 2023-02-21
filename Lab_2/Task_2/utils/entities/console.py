from .user import User
from ..constants.messages import \
        WELCOME_MESSAGE, \
        CLI_MESSAGE, \
        INVALID_COMMAND_MESSAGE
from ..constants.types import Command


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
    def user(self):
        return self.__user

    @user.setter
    def user(self, new_username):
        self.user = User(new_username)

    @property
    def commands(self):
        return self.__commands

    @staticmethod
    def parse_cmd():
        raw_command = input(CLI_MESSAGE).split(maxsplit=1)

        return raw_command[0], \
            (raw_command[-1], tuple(raw_command[-1].split()))[' ' in raw_command[-1]] if len(raw_command) > 1 else ''

    def run(self, command, args):
        if command not in self.commands:
            print(INVALID_COMMAND_MESSAGE)
        else:
            self.commands[command](args) if args else self.commands[command]()

    def start_session(self):
        print(WELCOME_MESSAGE)
        
        while True:
            command, args = self.parse_cmd()
            self.run(command, args)
