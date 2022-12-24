# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 6
#       udts = 0
#    opcodes = 24
#        ---   ABNF original opcodes
#        ALT = 0
#        CAT = 4
#        REP = 3
#        RNM = 11
#        TLS = 3
#        TBS = 0
#        TRG = 0
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 1
#        NOT = 2
#        BKA = 0
#        BKN = 0
#        BKR = 0
#        ABG = 0
#        AEN = 0
# characters = [97 - 99]
#

# RULES
rules = ({'name': 'S',
  'lower': 's',
  'index': 0,
  'line': 4,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 6, 8, 9)},
              {'type': 12},
              {'type': 2, 'children': (3, 4)},
              {'type': 4, 'index': 4},
              {'type': 13},
              {'type': 4, 'index': 2},
              {'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 4, 'index': 1},
              {'type': 4, 'index': 5},
              {'type': 13},
              {'type': 4, 'index': 3})},
 {'name': 'aa',
  'lower': 'aa',
  'index': 1,
  'line': 5,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (97,)},)},
 {'name': 'bb',
  'lower': 'bb',
  'index': 2,
  'line': 6,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (98,)},)},
 {'name': 'cc',
  'lower': 'cc',
  'index': 3,
  'line': 7,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (99,)},)},
 {'name': 'A',
  'lower': 'a',
  'index': 4,
  'line': 8,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 4)},
              {'type': 4, 'index': 1},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 4},
              {'type': 4, 'index': 2})},
 {'name': 'B',
  'lower': 'b',
  'index': 5,
  'line': 9,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 4)},
              {'type': 4, 'index': 2},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 5},
              {'type': 4, 'index': 3})})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False

def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += ";\n"
    sabnf += "; Language L = {a**nb**nc**n|n>=1}\n"
    sabnf += "; WikiPedia (https://en.wikipedia.org/wiki/Syntactic_predicate)\n"
    sabnf += ";\n"
    sabnf += "S = &(A !bb) 1*aa B !cc\n"
    sabnf += "aa = %s\"a\"\n"
    sabnf += "bb = %s\"b\"\n"
    sabnf += "cc = %s\"c\"\n"
    sabnf += "A = aa [A] bb\n"
    sabnf += "B = bb [B] cc\n"
    return sabnf

