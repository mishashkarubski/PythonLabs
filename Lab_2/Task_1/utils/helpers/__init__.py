""" A module for text processing and analysis.

Contains necessary text reading and parsing functions,
such as read_text or remove_punctuation
"""


import os
from ..constants import PUNCT_MARKS, TERM_MARKS


def read_text(user_input: str) -> str:
    """Either read the text from a file of specified path,
    or reads it from user's direct input.

    :argument user_input any string input.
    """
    if not os.path.lexists(user_input):
        return user_input

    with open(user_input, 'r') as file:
        return file.read()


def remove_punctuation(text: str) -> str:
    """Removes any punctuation from the text and returns words only."""

    return "".join(filter(lambda x: x not in PUNCT_MARKS + TERM_MARKS, text))
