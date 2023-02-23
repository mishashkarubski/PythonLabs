"""This module stores messages for interaction with CLI.

INFO_MSG displays info about CLI commands.
START_MESSAGE displays greeting.
CLI_INPUT marks where CLI waits for user's input.
INVALID_COMM_MESSAGE is displayed if entered command is invalid.
INVALID_ARG_MESSAGE is displayed if arguments do not correspond with command.
END_MESSAGE displays farewell.
SAVE_QUESTION asks whether user wants to save their container before leaving.
LOAD_QUESTION asks if user wants to load their container.
INVALID_QUESTION_RESPONSE indicates that user has responded incorrectly"
"""
from .types import Command

COMMAND_INFO = {
    Command.add.value: "<key> [key, ...] – adds one or more elements to container;",
    Command.remove.value: "<key> – delete key from container;",
    Command.find.value: "<key> [key, ...] – checks if the element is presented in the container;",
    Command.list.value: "– returns all elements of container;",
    Command.grep.value: "<regex> – check the value in the container by regular expression;",
    Command.save.value: "– saves container to file;",
    Command.load.value: "– loads container from file;",
    Command.switch.value: "– switches to another user.",
}
INFO_MSG = "\n".join([f"{comm} {COMMAND_INFO[comm]}" for comm in COMMAND_INFO])

MESSAGES = {
    'START_MESSAGE': f'''Welcome to Aboba CLI! Use ^C to exit. List of available commands:

    {INFO_MSG}
    ''',
    'CLI_INPUT': "~ ",
    'INVALID_COMM_MESSAGE': "No such command: {}. Skipping...",
    'INVALID_ARG_MESSAGE': "Invalid arguments: {}. Skipping...",
    'END_MESSAGE': "\nBoodgye (Cool Bug's fact: one day you will answer for your actions)!",
    'SAVE_QUESTION': "\nWould you like to save your storage? [y/n]: ",
    'LOAD_QUESTION': "Would you like to load container for user {}? [y/n]: ",
    'INVALID_RESPONSE': "Invalid response. Aborting...",
}
