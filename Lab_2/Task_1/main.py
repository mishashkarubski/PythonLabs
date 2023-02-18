"""Main module of Lab_2/Task_1"""
from utils import helpers
from utils.helpers import words, sentences


def main():
    """Carries out the subtasks of Task_1"""

    user_input = str(input(
        "Either enter the text manually " +
        "or specify the path to file with it: "
    ))

    text = helpers.read_text(user_input)

    print("Average word length in text (in chars) is",
          f"{words.average_word_length(text)}")
    print("Numbers of sentences in the text is",
          f"{sentences.count_sentences(text)}")
    print("Numbers of non-declarative sentences in the text is",
          f"{sentences.count_non_declarative(text)}")
    print("Average sentence lenth in text (in chars) is",
          f"{sentences.average_sentence_length(text)}")


if __name__ == '__main__':
    main()
