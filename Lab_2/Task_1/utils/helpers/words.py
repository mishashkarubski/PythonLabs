"""Contains functions for word processing."""
from ..constants import PRECISION, SPECIAL_CHARS
from ..helpers import remove_punctuation


def is_word(word: str) -> bool:
    """Checks if the given string is a word.

    Word consists of either letters only or letters and numbers.
    Word cannot consist only of numbers. All letters in the word must be latin.

    :argument word any string
    """
    return (not set(word) & SPECIAL_CHARS) and not word.isdigit()


def average_word_length(text: str) -> float:
    """Returns average word length (in characters) in the text
    :argument text any string
    """

    words = list(filter(is_word, remove_punctuation(text).split()))
    letters = "".join(words)

    try:
        return round(len(letters) / len(words), PRECISION)
    except ZeroDivisionError:
        return 0
