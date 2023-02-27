"""Contains functions for word processing."""
from . import process_text
from ..constants import PRECISION
import re


def get_words(text: str) -> list[str]:
    """Extracts words out of text."""
    text = process_text(text)
    return list(filter(lambda x: not x.isdigit(), re.findall(r"\w+", text)))


def average_word_length(text: str) -> float:
    """Returns average word length (in characters) in the text"""

    words = get_words(process_text(text))

    try:
        return round(len("".join(words)) / len(words), PRECISION)
    except ZeroDivisionError:
        return 0
