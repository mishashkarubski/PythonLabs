"""Part of helpers package. Functions for sentence processing."""


from ..constants import TERM_MARKS


def counter_factory(punct_marks: tuple[str]) -> object:
    """
    Returns a function which counts sentences with respect to
    specified punctuation marks.
    """
    def sentence_counter(text) -> int:
        """Counts the number of sentences in the given text."""

        text_length = len(text)
        text += " "

        return sum(
            char in punct_marks
            and (text[ind + 1] not in punct_marks or ind >= len(text) - 1)
            for ind, char in zip(range(text_length), list(text))
        )

    return sentence_counter


# Sentence counters (all & non-declarative)
count_sentences = counter_factory(TERM_MARKS)
count_non_declarative = counter_factory(TERM_MARKS[1:])


def average_sentence_length(text: str) -> int:
    """
    This function takes text as an input and returns
    the average sentence length in it (counting words only).
    """
    pass
