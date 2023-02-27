""" A module for text processing and analysis.

Contains necessary text reading and parsing functions,
such as read_text or process_text
"""
import os
from ..constants import (SPECIAL_CHARS)


def read_text(user_input: str) -> str:
    """Either read the text from a file of specified path,

    or reads it from user's direct input.
    """
    if not os.path.lexists(user_input):
        return process_text(user_input)

    with open(user_input, 'r') as file:
        return process_text(file.read())


def process_text(text: str) -> str:
    """Leaves only latin letters, separators, and numbers in the given text"""

    return "".join(filter(lambda x: x not in SPECIAL_CHARS, text))
