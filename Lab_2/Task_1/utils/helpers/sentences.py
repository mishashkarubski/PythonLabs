"""Contains functions for sentence processing."""
import re

from . import process_text
from .words import get_words
from ..constants import TERM_MARKS, PRECISION


def is_sentence(sentence: str) -> bool:
    """Verifies if the given piece of text is a sentence."""
    return bool(re.search(r"[A-z]", sentence))


def get_sentences(text: str, term_marks: str = TERM_MARKS) -> list[str]:
    """Returns list of sentences from the text."""

    return list(filter(
        is_sentence,
        re.findall(rf"[^{term_marks}]+[{term_marks}]", process_text(text))
    ))


def count_sentences(text: str, term_marks: str = TERM_MARKS) -> int:
    """Counts the number of sentences in the given text."""
    return len(get_sentences(process_text(text), term_marks))


def average_sentence_length(text: str) -> float:
    """Average sentence length in text in characters (counting words only)."""

    sentence_lens = map(
        lambda words: len("".join(words)),
        map(get_words, get_sentences(text))
    )

    try:
        return round(sum(sentence_lens) / count_sentences(text), PRECISION)
    except ZeroDivisionError:
        return 0
