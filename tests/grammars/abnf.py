# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 4
#       udts = 0
#    opcodes = 12
#        ---   ABNF original opcodes
#        ALT = 1
#        CAT = 2
#        REP = 1
#        RNM = 3
#        TLS = 2
#        TBS = 2
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
# characters = [65 - 1024]
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
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 3})},
 {'name': 'rtbs',
  'lower': 'rtbs',
  'index': 1,
  'line': 1,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (65,)},
              {'type': 6, 'string': (66,)})},
 {'name': 'rtls',
  'lower': 'rtls',
  'index': 2,
  'line': 2,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 7, 'string': (99,)},
              {'type': 7, 'string': (100,)})},
 {'name': 'rtrg',
  'lower': 'rtrg',
  'index': 3,
  'line': 3,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 5, 'min': 123, 'max': 1024},)})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False

def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += "abnf = rtbs / rtls / *rtrg\n"
    sabnf += "rtbs = %d65 %d66\n"
    sabnf += "rtls = \"C\" \"D\"\n"
    sabnf += "rtrg = %d123-1024\n"
    sabnf += "\n"
    return sabnf

