# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 6
#       udts = 0
#    opcodes = 15
#        ---   ABNF original opcodes
#        ALT = 0
#        CAT = 3
#        REP = 0
#        RNM = 5
#        TLS = 3
#        TBS = 0
#        TRG = 0
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 2
#        BKN = 0
#        BKR = 2
#        ABG = 0
#        AEN = 0
# characters = [97 - 120]
#

# RULES
rules = ({'name': 'bkr-start',
  'lower': 'bkr-start',
  'index': 0,
  'line': 4,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 3)},
              {'type': 15},
              {'type': 4, 'index': 2},
              {'type': 4, 'index': 1})},
 {'name': 'abc',
  'lower': 'abc',
  'index': 1,
  'line': 5,
  'is_bkru': True,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (97, 98, 99)},)},
 {'name': 'bkr-rule',
  'lower': 'bkr-rule',
  'index': 2,
  'line': 6,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 3},
              {'type': 14,
               'name': 'x',
               'lower': 'x',
               'bkr_case': 604,
               'bkr_mode': 601,
               'is_udt': False,
               'empty': None,
               'index': 3})},
 {'name': 'x',
  'lower': 'x',
  'index': 3,
  'line': 7,
  'is_bkru': True,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 7, 'string': (120,)},)},
 {'name': 'tls-start',
  'lower': 'tls-start',
  'index': 4,
  'line': 11,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3)},
              {'type': 4, 'index': 5},
              {'type': 4, 'index': 1},
              {'type': 14,
               'name': 'abc',
               'lower': 'abc',
               'bkr_case': 604,
               'bkr_mode': 601,
               'is_udt': False,
               'empty': None,
               'index': 1})},
 {'name': 'tls-main',
  'lower': 'tls-main',
  'index': 5,
  'line': 12,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 15}, {'type': 7, 'string': (120, 120)})})

# UDTS
udts = ()

has_bkru = True
has_bkrr = False

def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += ";\n"
    sabnf += "; in theory should match sub string \"abc\" of \"xxabc \n"
    sabnf += "; as start rule should fail because of back reference\n"
    sabnf += "; in look behind\n"
    sabnf += "bkr-start = &&bkr-rule abc\n"
    sabnf += "abc = \"abc\"\n"
    sabnf += "bkr-rule = x \\x\n"
    sabnf += "x = \"x\"\n"
    sabnf += ";\n"
    sabnf += "; as start rule should match \"xxabcabc\"\n"
    sabnf += "; parsing substring 2:0\n"
    sabnf += "tls-start = tls-main abc \\abc\n"
    sabnf += "tls-main = &&\"xx\"\n"
    return sabnf

