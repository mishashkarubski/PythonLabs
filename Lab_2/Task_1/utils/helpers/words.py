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


def top_k_n_grams(text: str, n: int = 4, k: int = 10) -> list[str]:
    """Returns top-K repeated N-grams in the text"""

    words = get_words(process_text(text))
    n_grams = tuple(tuple(words[i:i+n]) for i in range(len(words)) if i + n < len(words))
    unique_n_grams = sorted(set(n_grams), key=n_grams.count, reverse=True)

    return [" ".join(n_gram) for n_gram in unique_n_grams[:k]]
