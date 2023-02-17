import utils.helpers.sentences as sents
import utils.helpers.words as words
import utils.helpers as helpers


def main():
    user_input = str(input("Either enter the text manually or specify the path to file with it: "))
    text = helpers.read_text(user_input)
    print(f"Average word lenth in text (in chars) is {words.average_word_length(text)}")
    print(f"Numbers of sentences in the text is {sents.count_sentences(text)}")
    print(f"Numbers of non-declarative sentences in the text is {sents.count_non_declarative(text)}")


if __name__ == '__main__':
    main()
