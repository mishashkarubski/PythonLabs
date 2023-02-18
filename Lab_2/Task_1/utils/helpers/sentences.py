"""Contains functions for sentence processing."""

from typing import Callable
from string import ascii_letters
from . import remove_punctuation
from .words import is_word
from ..constants import TERM_MARKS, PRECISION


def is_sentence(sentence: str) -> bool:
    """Checks if the given string is a word.

    Sentence must have at least one word.
    :argument sentence any string
    """
    sentence = remove_punctuation(sentence)

    return len(list(filter(is_word, sentence))) > 0


def counter_factory(term_marks: tuple[str]) -> Callable:
    """ Returns a function which counts sentences.

    Sentences are marked by the given punctuation marks.

    :argument term_marks tuple of strings, for instance ('.', '!', '?').
    """
    def sentence_counter(text: str) -> int:
        """Counts the number of sentences in the given text.
        :argument text any string.
        """
        words = text.split()
        inner_words = remove_punctuation(text).split()
        ending_words = list(filter(
            lambda w: w not in inner_words and w[0] in ascii_letters,
            words
        ))

        return len(list(filter(lambda w: w[-1] in term_marks, ending_words)))

    return sentence_counter


count_sentences = counter_factory(TERM_MARKS)
count_non_declarative = counter_factory(TERM_MARKS[1:])


def average_sentence_length(text: str) -> float:
    """ Average sentence length in text (counting words only).
    :argument text any string
    """
    sentences = list(filter(
        is_sentence,
        text.replace("!", ".").replace("?", ".").split(".")
    ))  # Splitting text into sentences and removing non-sentence results

    letters = "".join(
        "".join(filter(is_word, remove_punctuation(sentence).split()))
        for sentence in sentences
    )  # Removing non-words in sentences and concatenating the words

    try:
        result = round(len(letters) / count_sentences(text), PRECISION)
    except ZeroDivisionError:
        result = 0

    return result
