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


def top_k_n_grams(text: str, n: int = 4, k: int = 10) -> list[str]:
    """Returns top-K repeated N-grams in the text"""

    # text_words = words.get_words(text)
    # n_grams = [(words[i:i+n]) for i in range(len(text_words)) if i + n < len(text_words)]
    # unique_n_grams = list(set(n_grams))
    #
    # unique_n_grams = list(sorted(
    #     unique_n_grams,
    #     key=n_grams.count,
    #     reverse=True
    # ))
    #
    # return [" ".join(n_gram) for n_gram in unique_n_grams[:k]]
    pass
