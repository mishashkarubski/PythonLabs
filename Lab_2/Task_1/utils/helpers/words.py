"""Contains functions for word processing."""


from ..helpers import remove_punctuation


def is_word(word: str) -> bool:
    """Checks if the given string is a word.

    Word consists of either letters only or letters and numbers.
    Word cannot consist only of numbers. All letters in the word must be latin.

    :argument word any string
    """
    return word.isalnum() and not word.isdigit()


def average_word_length(text: str) -> float:
    """Returns average word length (in characters) in the text
    :argument text any string
    """

    words = list(filter(is_word, remove_punctuation(text).split()))

    return sum((map(len, words))) / len(words)
