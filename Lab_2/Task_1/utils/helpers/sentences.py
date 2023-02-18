"""Contains functions for sentence processing."""


from ..constants import TERM_MARKS


def counter_factory(punct_marks: tuple[str]) -> object:
    """ Returns a function which counts sentences.

    Sentences are marked by the given punctuation marks.
    :argument punct_marks tuple of strings, for instance ('.', '!', '?').
    """
    def sentence_counter(text: str) -> int:
        """Counts the number of sentences in the given text.
        :argument text any string.
        """
        text_length = len(text)
        text += " "

        return sum(
            char in punct_marks
            and (text[ind + 1] not in punct_marks or ind >= len(text) - 1)
            for ind, char in zip(range(text_length), list(text))
        )

    return sentence_counter


count_sentences = counter_factory(TERM_MARKS)
count_non_declarative = counter_factory(TERM_MARKS[1:])


def average_sentence_length(text: str) -> float:
    """ Average sentence length in characters it (counting words only)
    :argument text any string
    """
    pass
