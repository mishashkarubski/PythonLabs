import os
from constants import PUNCTUATION_MARKS, TERMINATION_MARKS


def read_text(user_input: str | os.PathLike) -> str:
    """
    This function is designed to get text either from file
    of specified path, or from the user's direct input.
    """
    if not os.path.lexists(user_input):
        return user_input

    with open(user_input, 'r') as file:
        return file.read()


def trim(text: str) -> str:
    """
    Removes any punctuation from the text and return a string
    consisting only of words.
    """
    return "".join(list(filter(lambda c: c not in PUNCTUATION_MARKS + TERMINATION_MARKS, text)))


def average_word_length(text: str) -> float:
    """
    This function takes text as an input and returns
    the average word length in it.
    """
    words = trim(text).split()

    return int(sum(len(word) for word in words) / len(words))
