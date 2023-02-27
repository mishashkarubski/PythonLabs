import unittest
import utils.helpers.words as words
import utils.helpers.sentences as sentences


class TestAverageWordLength(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(words.average_word_length(
            "  .. . . . .. !?? !?? ? !? ! ?! "), 0)
        self.assertEqual(words.average_word_length(
            ""), 0)

    def test_one_letter(self):
        self.assertEqual(words.average_word_length(
            "A"), 1)

    def test_one_word_many_letters(self):
        self.assertEqual(words.average_word_length(
            "COOLBUGSFACTONEDAYYOUWILLANSWERFORYO- -URACTIONS"), 22.5)

    def test_many_words_many_letters(self):
        self.assertEqual(words.average_word_length(
            "abba sus 124912 imp0ster"), 5)


class TestCountSentences(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(sentences.count_sentences(
            "  .. . . . .. !??-!?? ? !? ! ?! a wire"), 0)
        self.assertEqual(sentences.count_sentences(
            ""), 0)

    def test_one_sentence(self):
        # self.assertEqual(sentences.count_sentences(
        #     "a."), 1)
        self.assertEqual(sentences.count_sentences(
            " _ .. /  _  @A@.  ;;;"), 1)

    def test_one_sentence_many_words(self):
        self.assertEqual(sentences.count_sentences(
            "COOL BUGS FACT: ONE DAY 14 YOU WILL ___`14gaAB{}0 ANSWER FOR YOUR ACTIONS."), 1)

    def test_many_sentences_many_words(self):
        self.assertEqual(sentences.count_sentences(
            "a b. c?? abba!! abba,   aboba... bobA AA..?    .! . .?? . skdjf> as."), 6)


class TestCountNonDeclarative(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(sentences.count_non_declarative(
            "  .. . . . .. !?? !?? ? !? ! ?! "), 0)
        self.assertEqual(sentences.count_non_declarative(
            ""), 0)

    def test_one_non_declarative(self):
        self.assertEqual(sentences.count_non_declarative(
            "a...!??!!??!?!"), 1)
        self.assertEqual(sentences.count_non_declarative(
            " _ .. /  _  @A@.   A12..A12.!??!!?     B1500     ;;;"), 1)

    def test_many_non_declarative_many_signs(self):
        self.assertEqual(sentences.count_non_declarative(
            "a...!?? ----!!?? a b!? c..!"), 3)

    def test_many_sentences_many_words(self):
        self.assertEqual(sentences.count_non_declarative(
            "a b. c? abba!! abba, .. bobA AA..?    .! . .?? . skdjf> as."), 3)


class TestAverageSentenceLength(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(sentences.average_sentence_length(
            "  .. . . . .. !?? !?? ? !? ! ?! "), 0)
        self.assertEqual(sentences.average_sentence_length(
            ""), 0)

    def test_one_char_long(self):
        self.assertEqual(sentences.average_sentence_length(
            "a...!??!!??!?!"), 1)
        self.assertEqual(sentences.average_sentence_length(
            " @-@. .?.?.?!  A. 14 "), 1)

    def test_two_sentences_many_words(self):
        self.assertEqual(sentences.average_sentence_length(
            "COOL BUGS 98123749812374 FACT: ONE DAY 14 YOU WILL. 0 ANSWER ___FOR YOUR ACTIONS."), 22.5)

    def test_many_sentences_many_words(self):
        self.assertEqual(sentences.average_sentence_length(
            "a b. c? abba!! abba, .. bobA AA..?    .! . .?? . skdjf> as."), 4)
