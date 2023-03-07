"""Constants of the 'utils' package"""
import string

# Punctuation constants
TERM_MARKS = '.!?'
PUNCT_MARKS = ',;-–'

# Round precision for average length functions
PRECISION = 2

# Non-letters (except punctuation)
SPECIAL_CHARS = set(string.punctuation) - (set(TERM_MARKS) | set(PUNCT_MARKS))

# Abbreviations
ABBREVIATIONS = '''dr. jr. sr. mr. ms. mrs. in. ft. etc. e.g. 
i.e. a.d. b.c. c.e. b.c.e. inc. a.m. p.m.'''
