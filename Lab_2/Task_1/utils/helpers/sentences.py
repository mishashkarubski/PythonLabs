"""Contains functions for sentence processing."""
import re

from . import process_text
from .words import get_words
from ..constants import TERM_MARKS


def is_sentence(sentence: str) -> bool:
    """Verifies if the given piece of text is a sentence."""
    return bool(re.search("[A-z]", sentence)) and sentence[-1] in TERM_MARKS


def count_sentences(text: str) -> int:
    """Counts the number of sentences in the given text."""
    # print(re.findall(f"[^{TERM_MARKS}]+[{TERM_MARKS}]", text))
    # print(list(filter(is_sentence, re.findall(f"[^{TERM_MARKS}]+[{TERM_MARKS}]", text))))
    text = process_text(text)

    return len(list(filter(
        is_sentence,
        re.findall(f"[^{TERM_MARKS}]+[{TERM_MARKS}]", text)
    )))


def count_non_declarative(text: str) -> int:
    """Counts the number of sentences in the given text."""

    text = process_text(text)

    return len(list(filter(
        is_sentence, re.findall(f"[^{TERM_MARKS[1:]}]+[{TERM_MARKS[1:]}]", text)
    )))


def average_sentence_length(text: str) -> float:
    """Average sentence length in text in characters (counting words only)."""

    text = process_text(text)
    sentences = list(map(get_words, re.findall(f"[^{TERM_MARKS}]+", text)))
    sentence_chars = ["".join(sent_words) for sent_words in sentences]

    try:
        return sum(map(len, sentence_chars)) / count_sentences(text)
    except ZeroDivisionError:
        return 0
