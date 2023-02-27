"""Unit tests for helper functions of Lab_2/Task_1"""
import unittest

from utils.helpers.words import average_word_length
from utils.helpers.sentences import count_sentences, average_sentence_length
from utils.constants import TERM_MARKS


class TestAverageWordLength(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(average_word_length("  .. . .. !?? !? ? !? ?! "), 0)
        self.assertEqual(average_word_length(""), 0)

    def test_one_letter(self):
        self.assertEqual(average_word_length("A"), 1)

    def test_one_word_many_letters(self):
        self.assertEqual(average_word_length(
            "COOLBUGSFACTONEDAYYOUWILLANSWERFORYO- -URACTIONS"), 22.5)

    def test_many_words_many_letters(self):
        self.assertEqual(average_word_length("abba sus 124912 imp0ster"), 5)


class TestCountSentences(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(count_sentences(" .. . .. !??-- ? !? ! ?!a wire"), 0)
        self.assertEqual(count_sentences(""), 0)

    def test_one_sentence(self):
        self.assertEqual(count_sentences("a."), 1)
        self.assertEqual(count_sentences(" _ .. /  _  @A@.  ;;;"), 1)

    def test_one_sentence_many_words(self):
        self.assertEqual(count_sentences(
            "COOL BUGS FACT: ONE 14 YOU WILL ___`14gaAB{}0 FOR YOUR ACT."), 1)

    def test_many_sentences_many_words(self):
        self.assertEqual(count_sentences(
            "a b. c?? abba!! abba, aboba... bobA AA..?   .! ? . sjf> as."), 6)


class TestCountNonDeclarative(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(count_sentences(
            "  .. . . . .. !?? !?? ? !? ! ?! ", TERM_MARKS[1:]), 0)
        self.assertEqual(count_sentences(
            "", TERM_MARKS[1:]), 0)

    def test_one_non_declarative(self):
        self.assertEqual(count_sentences(
            "a...!??!!??!?!"), 1)
        self.assertEqual(count_sentences(
            " _ .. /  _  @A@.   A12..A12.!!!? B1500  ;;;", TERM_MARKS[1:]), 1)

    def test_many_non_declarative_many_signs(self):
        self.assertEqual(count_sentences(
            "a...!?? ----!!?? a b!? c..!", TERM_MARKS[1:]), 3)

    def test_many_sentences_many_words(self):
        self.assertEqual(count_sentences(
            "a b. c? abba!! abba, .. bobA AA..? .! . ?. sjf> as.",
            TERM_MARKS[1:]
        ), 3)


class TestAverageSentenceLength(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(average_sentence_length(
            "  .. . . . .. !?? !?? ? !? ! ?! "), 0)
        self.assertEqual(average_sentence_length(""), 0)

    def test_one_char_long(self):
        self.assertEqual(average_sentence_length("a...!??!!??!?!"), 1)
        self.assertEqual(average_sentence_length(" @-@. .?.?.?!  A. 14 "), 1)

    def test_two_sentences_many_words(self):
        self.assertEqual(average_sentence_length(
            """COOL BUGS 98123749812374 FACT: ONE DAY 14 YOU WILL
            . 0 ANSWER ___FOR YOUR ACTIONS."""), 22.5)

    def test_many_sentences_many_words(self):
        self.assertAlmostEqual(average_sentence_length(
            "a b. c? abba!! abba, .. bobA AA..? .! . ?. sjf> as."), 3.67)
