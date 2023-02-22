from .types import Command


COMMAND_INFO = {
    Command.add.value: "<key> [key, ...] – adds one or more elements to container;",
    Command.remove.value: "<key> – delete key from container;",
    Command.find.value: "<key> [key, ...] – checks if the element is presented in the container;",
    Command.list.value: "– returns all elements of container;",
    Command.grep.value: "<regex> – check the value in the container by regular expression;",
    Command.save.value: "– saves container to file;",
    Command.load.value:  "– loads container from file;",
    Command.switch.value: "– switches to another user.",
}
INFO_MSG = "\n".join([f"{comm} {COMMAND_INFO[comm]}" for comm in COMMAND_INFO])

START_MESSAGE = f'''Welcome to Aboba CLI! Use ^C to exit. List of available commands:

{INFO_MSG}

'''
CLI_INPUT = "~ "
INVALID_COMM_MESSAGE = "Invalid command. Skipping."
INVALID_PARAM_MESSAGE = "Invalid parameters. Skipping."
END_MESSAGE = "\nBoodgye!"
SAVE_QUESTION = "\nWould you like to save your storage? [y/n]: "
LOAD_QUESTION = "Would you like to load container for user {}? [y/n]: "
