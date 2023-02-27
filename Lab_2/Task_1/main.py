"""Main module of Lab_2/Task_1"""
from utils.helpers import read_text
from utils.helpers.words import (average_word_length, top_k_n_grams)
from utils.helpers.sentences import (count_sentences, average_sentence_length)
from utils.constants import TERM_MARKS


def main():
    """Carries out the subtasks of Task_1"""

    text = read_text(str(input(
        "Either enter the text manually " +
        "or specify the path to file with it: "
    )))
    n, k = 4, 10

    print("1. Average word length in text (in chars) is",
          f"{average_word_length(text)}")
    print("2. Numbers of sentences in the text is",
          f"{count_sentences(text)}")
    print("3. Numbers of non-declarative sentences in the text is",
          f"{count_sentences(text, TERM_MARKS[1:])}")
    print("4. Average sentence length in text (in chars) is",
          f"{average_sentence_length(text)}")
    print(f"5. Top {k} repeated {n}-grams are",
          f"{top_k_n_grams(text, n, k)}")


if __name__ == '__main__':
    main()
