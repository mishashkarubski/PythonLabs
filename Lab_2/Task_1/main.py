"""Main module of Lab_2/Task_1"""
from utils import helpers
from utils.helpers import words, sentences


def main():
    """Carries out the subtasks of Task_1"""

    text = helpers.read_text(str(input(
        "Either enter the text manually " +
        "or specify the path to file with it: "
    )))
    n, k = 4, 10

    print("1. Average word length in text (in chars) is",
          f"{words.average_word_length(text)}")
    print("2. Numbers of sentences in the text is",
          f"{sentences.count_sentences(text)}")
    print("3. Numbers of non-declarative sentences in the text is",
          f"{sentences.count_non_declarative(text)}")
    print("4. Average sentence lenth in text (in chars) is",
          f"{sentences.average_sentence_length(text)}")
    print(f"5. Top {k} repeated {n}-grams are",
          f"{helpers.top_k_n_grams(text, n, k)}")


if __name__ == '__main__':
    main()
