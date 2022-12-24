# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 6
#       udts = 0
#    opcodes = 12
#        ---   ABNF original opcodes
#        ALT = 1
#        CAT = 2
#        REP = 0
#        RNM = 5
#        TLS = 4
#        TBS = 0
#        TRG = 0
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 0
#        BKN = 0
#        BKR = 0
#        ABG = 0
#        AEN = 0
# characters = [97 - 122]
#

# RULES
rules = ({'name': 'start',
  'lower': 'start',
  'index': 0,
  'line': 0,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 1},
              {'type': 4, 'index': 4})},
 {'name': 'Left',
  'lower': 'left',
  'index': 1,
  'line': 1,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 4, 'index': 2},
              {'type': 4, 'index': 3})},
 {'name': 'Alt1',
  'lower': 'alt1',
  'index': 2,
  'line': 2,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 5},
              {'type': 7, 'string': (97, 98, 99)})},
 {'name': 'Alt2',
  'lower': 'alt2',
  'index': 3,
  'line': 3,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (120, 121, 122)},)},
 {'name': 'Right',
  'lower': 'right',
  'index': 4,
  'line': 4,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (120, 121, 122)},)},
 {'name': 'X',
  'lower': 'x',
  'index': 5,
  'line': 5,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (120, 121, 122)},)})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False

def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += "start = Left Right\n"
    sabnf += "Left  = Alt1 / Alt2\n"
    sabnf += "Alt1  = (X \"abc\")\n"
    sabnf += "Alt2  = \"xyz\"\n"
    sabnf += "Right = \"xyz\"\n"
    sabnf += "X     = \"xyz\"\n"
    return sabnf

