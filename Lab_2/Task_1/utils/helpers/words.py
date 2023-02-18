"""Part of helpers package. Functions for word processing."""


from ..helpers import remove_punctuation


def is_word(word: str) -> bool:
    """
    Single word validation function. Word consists of either letters
    or letters and numbers. Word cannot consist only of numbers.
    All letters in the word must be latin.
    """
    return word.isalnum() and not word.isdigit()


def average_word_length(text: str) -> int:
    """
    This function takes text as an input and returns
    the average word length in it.
    """
    words = list(filter(is_word, remove_punctuation(text).split()))

    return int(sum((map(len, words))) / len(words))
