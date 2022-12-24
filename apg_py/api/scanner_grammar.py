# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 10
#       udts = 0
#    opcodes = 31
#        ---   ABNF original opcodes
#        ALT = 5
#        CAT = 2
#        REP = 4
#        RNM = 11
#        TLS = 0
#        TBS = 4
#        TRG = 5
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 0
#        BKN = 0
#        BKR = 0
#        ABG = 0
#        AEN = 0
# characters = [0 - 9223372036854775807]
#

# RULES
rules = ({'name': 'file',
  'lower': 'file',
  'index': 0,
  'line': 0,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 3)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 1},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 3})},
 {'name': 'line',
  'lower': 'line',
  'index': 1,
  'line': 1,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 2},
              {'type': 4, 'index': 6})},
 {'name': 'line-text',
  'lower': 'line-text',
  'index': 2,
  'line': 2,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3)},
              {'type': 4, 'index': 4},
              {'type': 4, 'index': 5})},
 {'name': 'last-line',
  'lower': 'last-line',
  'index': 3,
  'line': 3,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3)},
              {'type': 4, 'index': 4},
              {'type': 4, 'index': 5})},
 {'name': 'valid',
  'lower': 'valid',
  'index': 4,
  'line': 4,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 5, 'min': 32, 'max': 126},
              {'type': 6, 'string': (9,)})},
 {'name': 'invalid',
  'lower': 'invalid',
  'index': 5,
  'line': 5,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3, 4)},
              {'type': 5, 'min': 0, 'max': 8},
              {'type': 5, 'min': 11, 'max': 12},
              {'type': 5, 'min': 14, 'max': 31},
              {'type': 5, 'min': 127, 'max': 9223372036854775807})},
 {'name': 'end',
  'lower': 'end',
  'index': 6,
  'line': 6,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 4, 'index': 7},
              {'type': 4, 'index': 8},
              {'type': 4, 'index': 9})},
 {'name': 'CRLF',
  'lower': 'crlf',
  'index': 7,
  'line': 7,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (13, 10)},)},
 {'name': 'LF',
  'lower': 'lf',
  'index': 8,
  'line': 8,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (10,)},)},
 {'name': 'CR',
  'lower': 'cr',
  'index': 9,
  'line': 9,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (13,)},)})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False


def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += "file = *line [last-line]\n"
    sabnf += "line = line-text end\n"
    sabnf += "line-text = *(valid/invalid)\n"
    sabnf += "last-line = 1*(valid/invalid)\n"
    sabnf += "valid = %d32-126 / %d9\n"
    sabnf += "invalid = %d0-8 / %d11-12 /%d14-31 / %x7f-7FFFFFFFFFFFFFFF\n"
    sabnf += "end = CRLF / LF / CR\n"
    sabnf += "CRLF = %d13.10\n"
    sabnf += "LF = %d10\n"
    sabnf += "CR = %d13\n"
    return sabnf

