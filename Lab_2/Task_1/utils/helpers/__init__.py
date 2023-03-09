""" A module for text processing and analysis.

Contains necessary text reading and parsing functions,
i.e. read_text, process_text and multireplace
"""
import os
import re
from ..constants import SPECIAL_CHARS, ABBREVIATIONS


def read_text(user_input: str) -> str:
    """Either read the text from a file of specified path,
    or reads it from user's direct input.
    """
    if not os.path.lexists(user_input):
        return process_text(user_input)

    with open(user_input, 'r', encoding='utf-8') as file:
        return process_text(file.read())


def multireplace(text: str, replace_dict: dict[str]) -> str:
    """Replaces multiple substrings according to the
    given replacement mapping
    :param text: any string that needs to be partially replaced
    :param replace_dict: replacement mapping of old values to new ones
    """
    replace_dict = {
        re.escape(key.lower()): val
        for key, val in replace_dict.items()
    }
    pattern = re.compile("|".join(replace_dict.keys()), re.IGNORECASE)

    return pattern.sub(lambda m: replace_dict[re.escape(m.group().lower())], text)


def process_text(text: str) -> str:
    """Leaves only latin letters, separators, and numbers in the given text"""

    text = multireplace(text, {
        abbr: abbr.replace(".", "")
        for abbr in ABBREVIATIONS.split()
    })

    return "".join(filter(lambda char: char not in SPECIAL_CHARS, text))
