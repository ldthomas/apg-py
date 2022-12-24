# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 4
#       udts = 0
#    opcodes = 10
#        ---   ABNF original opcodes
#        ALT = 1
#        CAT = 1
#        REP = 1
#        RNM = 3
#        TLS = 2
#        TBS = 1
#        TRG = 1
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 0
#        BKN = 0
#        BKR = 0
#        ABG = 0
#        AEN = 0
# characters = [67 - 255]
#

# RULES
rules = ({'name': 'abnf',
  'lower': 'abnf',
  'index': 0,
  'line': 0,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 4, 'index': 1},
              {'type': 4, 'index': 2},
              {'type': 4, 'index': 3})},
 {'name': 'tls',
  'lower': 'tls',
  'index': 1,
  'line': 1,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 7, 'string': (97,)},
              {'type': 7, 'string': (98,)})},
 {'name': 'tbs',
  'lower': 'tbs',
  'index': 2,
  'line': 2,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (67, 68)},)},
 {'name': 'trg',
  'lower': 'trg',
  'index': 3,
  'line': 3,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 5, 'min': 128, 'max': 255})})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False


def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += "abnf = tls / tbs/ trg\n"
    sabnf += "tls = \"A\" \"B\"\n"
    sabnf += "tbs = %d67.68\n"
    sabnf += "trg = 1*%d128-255\n"
    return sabnf

