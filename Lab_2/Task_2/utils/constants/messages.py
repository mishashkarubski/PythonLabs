"""This module stores messages for interaction with CLI.

CLI_INFO displays info about CLI commands.
START_MESSAGE displays greeting.
CLI_INPUT marks where CLI waits for user's input.
INVALID_COMM_MESSAGE is displayed if entered command is invalid.
INVALID_ARG_MESSAGE is displayed if arguments do not correspond with command.
END_MESSAGE displays farewell.
USERNAME_REQUEST asks for user's name
SAVE_QUESTION asks whether user wants to save their container before leaving.
LOAD_QUESTION asks if user wants to load their container.
INVALID_RESPONSE indicates that user has responded incorrectly
"""
from .types import Command

CLI_INFO: dict[Command, str] = {
    Command.add.value: "<key> [key, ...] – adds one or more elements to container;",
    Command.remove.value: "<key> – delete key from container;",
    Command.find.value: "<key> [key, ...] – checks if the element is presented in the container;",
    Command.list.value: "– returns all elements of container;",
    Command.grep.value: "<regex> – check the value in the container by regular expression;",
    Command.save.value: "– saves container to file;",
    Command.load.value: "– loads container from file;",
    Command.switch.value: "– switches to another user.",
}
INFO_MSG: str = "\n".join([f"{comm} {CLI_INFO[comm]}" for comm in CLI_INFO.keys()])

# Messages for CLI I/O in interactive mode
START_MESSAGE: str = f'''Welcome to Aboba CLI! Use ^C to exit. List of available commands:

{INFO_MSG}'''
CLI_INPUT: str = "~ "
INVALID_COMM_MESSAGE: str = "No such command: {}. Skipping..."
INVALID_ARG_MESSAGE: str = "Invalid arguments: {}. Skipping..."
END_MESSAGE: str = "\nBoodgye (Cool Bug's fact: one day you will answer for your actions)!"
USERNAME_REQUEST: str = "Username: "
SAVE_QUESTION: str = "\nWould you like to save your storage? [y/n]: "
LOAD_QUESTION: str = "Would you like to load storage for user {}? [y/n]: "
INVALID_RESPONSE: str = "Invalid response. Aborting..."
