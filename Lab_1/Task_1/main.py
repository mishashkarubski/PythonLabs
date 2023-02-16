import helpers


def main():
    user_input = str(input("Either enter the text manually or specify the path to file with it: "))
    text = helpers.read_text(user_input)
    print(helpers.average_word_length(text))


if __name__ == '__main__':
    main()
