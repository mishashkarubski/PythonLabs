import os
from collections import namedtuple
from constants import PUNCT_MARKS, TERM_MARKS


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
    return "".join(list(filter(lambda x: x not in PUNCT_MARKS + TERM_MARKS, text.strip())))


def average_word_length(text: str) -> int:
    """
    This function takes text as an input and returns
    the average word length in it.
    """
    words = list(filter(is_word, remove_punctuation(text).split()))

    return int(sum((map(len, words))) / len(words))


def counter_factory(punct_marks: tuple[str]) -> object:
    def _count_sentences(text) -> int:
        """
        Counts the number of sentences in text with respect
        to the given punctuation marks.
        """
        text_length = len(text)
        text += " "

        return sum(
            char in punct_marks and (text[ind + 1] not in punct_marks or ind >= len(text) - 1)
            for ind, char in zip(range(text_length), list(text))
        )

    return _count_sentences


count_sentences = counter_factory(TERM_MARKS)
count_non_declarative = counter_factory(TERM_MARKS[1:])
