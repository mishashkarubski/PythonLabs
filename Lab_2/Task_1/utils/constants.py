"""Constants of the 'utils' package"""
import string


# Punctuation constants
TERM_MARKS = ('.', '!', '?')
PUNCT_MARKS = (',', ';', '-', '–')

# Round precision for average length functions
PRECISION = 2

# Non-letter symbols
SPECIAL_CHARS = set(string.punctuation).difference(set(TERM_MARKS) & set(PUNCT_MARKS))
