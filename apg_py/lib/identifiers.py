""" @file apg_py/lib/identifiers.py
@brief All of the APG numerical ids.
"""

import sys

# use this for infinity
MAX_INT = sys.maxsize

# the original ABNF operators
ALT = 1  # alternation
CAT = 2  # concatenation
REP = 3  # repetition
RNM = 4  # rule name
TRG = 5  # terminal range
TBS = 6  # terminal binary string
TLS = 7  # terminal literal string, case insensitive

# the super set, SABNF operators
UDT = 11  # user - defined terminal
AND = 12  # positive look ahead
NOT = 13  # negative look ahead
BKR = 14  # back reference to previously matched rule/UDT
BKA = 15  # positive look behind
BKN = 16  # negative look behind
ABG = 17  # anchor - begin of string
AEN = 18  # anchor - end of string

# the parser states
ACTIVE = 100
MATCH = 101
EMPTY = 102
NOMATCH = 103

# AST translation states and call back function returns
SEM_PRE = 200  # AST down
SEM_POST = 201  # AST up
SEM_OK = 300  # AST normal return
SEM_SKIP = 301  # AST directs transator to skip branch below this node

# rule attribute categorization
ATTR_N = 400  # non-recursive
ATTR_R = 401  # recursive
ATTR_MR = 402  # belongs to a mutually-recursive set

# Look around values - indicate if parser is in look ahead or look behind mode.
LOOKAROUND_NONE = 500  # parser in normal parsing mode
LOOKAROUND_AHEAD = 501  # parser is in look-ahead mode
LOOKAROUND_BEHIND = 502  # parser is in look-behind mode

# Back reference rule mode indicators
BKR_MODE_UM = 601  # universal mode back reference
BKR_MODE_RM = 602  # recursive mode back reference
BKR_MODE_CS = 603  # back reference is case sensitive
BKR_MODE_CI = 604  # back reference is case insensitive

# dictionary to match names to ids
dict = {
    ALT: 'ALT',
    CAT: 'CAT',
    REP: 'REP',
    RNM: 'RNM',
    TRG: 'TRG',
    TBS: 'TBS',
    TLS: 'TLS',
    UDT: 'UDT',
    AND: 'AND',
    NOT: 'NOT',
    BKR: 'BKR',
    BKA: 'BKA',
    BKN: 'BKN',
    ABG: 'ABG',
    AEN: 'AEN',
    ACTIVE: 'ACTIVE',
    MATCH: 'MATCH',
    EMPTY: 'EMPTY',
    NOMATCH: 'NOMATCH',
    SEM_PRE: 'SEM_PRE',
    SEM_POST: 'SEM_POST',
    SEM_OK: 'SEM_OK',
    SEM_SKIP: 'SEM_SKIP',
    ATTR_N: 'ATTR_N',
    ATTR_R: 'ATTR_R',
    ATTR_MR: 'ATTR_MR',
    LOOKAROUND_NONE: 'LOOKAROUND_NONE',
    LOOKAROUND_AHEAD: 'LOOKAROUND_AHEAD',
    LOOKAROUND_BEHIND: 'LOOKAROUND_BEHIND',
    BKR_MODE_UM: 'BKR_MODE_UM',
    BKR_MODE_RM: 'BKR_MODE_RM',
    BKR_MODE_CS: 'BKR_MODE_CS',
    BKR_MODE_CI: 'BKR_MODE_CI',
}
