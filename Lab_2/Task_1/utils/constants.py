"""Constants of the 'utils' package"""
import string


# Punctuation constants
TERM_MARKS = '.!?'
PUNCT_MARKS = ',;-–'

# Round precision for average length functions
PRECISION = 2

# Non-letter symbols
SPECIAL_CHARS = set(string.punctuation) - (set(TERM_MARKS) | set(PUNCT_MARKS))

# Abbreviations
ABBREVIATIONS = ('mr.', 'ms.', 'mrs.', 'etc.', 'e.g.', 'i.e.', 'A.D.', 'B.C.', 'inc.')
