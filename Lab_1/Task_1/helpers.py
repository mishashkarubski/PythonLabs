import os
from constants import PUNCTUATION_MARKS, TERMINATION_MARKS


def is_word(word: str) -> bool:
    """
    Single word validation function. Word consists of either letters
    or letters and numbers. Word cannot consist only of numbers.
    All letters in the word must be latin.
    """
    return word.isalnum() and not word.isdigit()


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
    return "".join(list(filter(lambda x: x not in PUNCTUATION_MARKS + TERMINATION_MARKS, text)))


def average_word_length(text: str) -> int:
    """
    This function takes text as an input and returns
    the average word length in it.
    """
    words = list(filter(is_word, remove_punctuation(text).split()))

    return int(sum((map(len, words))) / len(words))
