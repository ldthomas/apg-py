# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 9
#       udts = 0
#    opcodes = 36
#        ---   ABNF original opcodes
#        ALT = 3
#        CAT = 5
#        REP = 7
#        RNM = 10
#        TLS = 6
#        TBS = 1
#        TRG = 3
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 1
#        BKN = 0
#        BKR = 0
#        ABG = 0
#        AEN = 0
# characters = [43 - 101]
#

# RULES
rules = ({'name': 'float',
  'lower': 'float',
  'index': 0,
  'line': 0,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 3, 4, 5)},
              {'type': 15},
              {'type': 6, 'string': (97, 98, 99)},
              {'type': 4, 'index': 1},
              {'type': 4, 'index': 2},
              {'type': 4, 'index': 6})},
 {'name': 'sign',
  'lower': 'sign',
  'index': 1,
  'line': 1,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (2, 3)},
              {'type': 7, 'string': (43,)},
              {'type': 7, 'string': (45,)})},
 {'name': 'decimal',
  'lower': 'decimal',
  'index': 2,
  'line': 2,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 7)},
              {'type': 2, 'children': (2, 3)},
              {'type': 4, 'index': 3},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 2, 'children': (5, 6)},
              {'type': 4, 'index': 4},
              {'type': 4, 'index': 5},
              {'type': 2, 'children': (8, 9)},
              {'type': 4, 'index': 4},
              {'type': 4, 'index': 5})},
 {'name': 'integer',
  'lower': 'integer',
  'index': 3,
  'line': 4,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 5, 'min': 48, 'max': 57})},
 {'name': 'dot',
  'lower': 'dot',
  'index': 4,
  'line': 5,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (46,)},)},
 {'name': 'fraction',
  'lower': 'fraction',
  'index': 5,
  'line': 6,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 5, 'min': 48, 'max': 57})},
 {'name': 'exponent',
  'lower': 'exponent',
  'index': 6,
  'line': 7,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 1},
              {'type': 2, 'children': (2, 3, 4)},
              {'type': 7, 'string': (101,)},
              {'type': 4, 'index': 7},
              {'type': 4, 'index': 8})},
 {'name': 'esign',
  'lower': 'esign',
  'index': 7,
  'line': 8,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (2, 3)},
              {'type': 7, 'string': (43,)},
              {'type': 7, 'string': (45,)})},
 {'name': 'exp',
  'lower': 'exp',
  'index': 8,
  'line': 9,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 5, 'min': 48, 'max': 57})})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False

def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += "float    = &&%d97.98.99 sign decimal exponent\n"
    sabnf += "sign     = [\"+\" / \"-\"]\n"
    sabnf += "decimal  = integer [dot fraction]\n"
    sabnf += "           / dot fraction\n"
    sabnf += "integer  = 1*%d48-57\n"
    sabnf += "dot      = \".\"\n"
    sabnf += "fraction = *%d48-57\n"
    sabnf += "exponent = [\"e\" esign exp]\n"
    sabnf += "esign    = [\"+\" / \"-\"]\n"
    sabnf += "exp      = 1*%d48-57\n"
    return sabnf

