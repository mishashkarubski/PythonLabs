import os
from ..constants import PUNCT_MARKS, TERM_MARKS


# Module name
__name__ = "__helpers__"


def read_text(user_input: str) -> str:
    """
    This function is designed to either read the text from a file
    of specified path, or read it from user's direct input.
    """
    if not os.path.lexists(user_input):
        return user_input

    with open(user_input, 'r') as file:
        return file.read()


def remove_punctuation(text: str) -> str:
    """
    Removes any punctuation from the text and returns a string
    consisting only of words.
    """
    return "".join(list(filter(lambda x: x not in PUNCT_MARKS + TERM_MARKS, text.strip())))
