# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 48
#       udts = 0
#    opcodes = 204
#        ---   ABNF original opcodes
#        ALT = 25
#        CAT = 18
#        REP = 19
#        RNM = 76
#        TLS = 11
#        TBS = 31
#        TRG = 24
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 0
#        BKN = 0
#        BKR = 0
#        ABG = 0
#        AEN = 0
# characters = [9 - 126]
#

# RULES
rules = ({'name': 'ini-file',
  'lower': 'ini-file',
  'index': 0,
  'line': 31,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 5)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (3, 4)},
              {'type': 4, 'index': 38},
              {'type': 4, 'index': 5},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 1})},
 {'name': 'section',
  'lower': 'section',
  'index': 1,
  'line': 32,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 2},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (4, 5)},
              {'type': 4, 'index': 38},
              {'type': 4, 'index': 5})},
 {'name': 'section-line',
  'lower': 'section-line',
  'index': 2,
  'line': 33,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 4, 'index': 3},
              {'type': 4, 'index': 4})},
 {'name': 'good-section-line',
  'lower': 'good-section-line',
  'index': 3,
  'line': 34,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4, 5, 6, 7, 9)},
              {'type': 7, 'string': (91,)},
              {'type': 4, 'index': 43},
              {'type': 4, 'index': 9},
              {'type': 4, 'index': 43},
              {'type': 7, 'string': (93,)},
              {'type': 4, 'index': 43},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 42},
              {'type': 4, 'index': 41})},
 {'name': 'bad-section-line',
  'lower': 'bad-section-line',
  'index': 4,
  'line': 35,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 4)},
              {'type': 7, 'string': (91,)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 47},
              {'type': 4, 'index': 41})},
 {'name': 'value-line',
  'lower': 'value-line',
  'index': 5,
  'line': 36,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 4, 'index': 6},
              {'type': 4, 'index': 7})},
 {'name': 'good-value',
  'lower': 'good-value',
  'index': 6,
  'line': 37,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4, 5, 6, 7, 9)},
              {'type': 4, 'index': 10},
              {'type': 4, 'index': 43},
              {'type': 7, 'string': (61,)},
              {'type': 4, 'index': 43},
              {'type': 4, 'index': 8},
              {'type': 4, 'index': 43},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 42},
              {'type': 4, 'index': 41})},
 {'name': 'bad-value-line',
  'lower': 'bad-value-line',
  'index': 7,
  'line': 38,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 4, 6)},
              {'type': 1, 'children': (2, 3)},
              {'type': 5, 'min': 33, 'max': 90},
              {'type': 5, 'min': 92, 'max': 126},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 47},
              {'type': 4, 'index': 41})},
 {'name': 'value-array',
  'lower': 'value-array',
  'index': 8,
  'line': 39,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 11},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 2, 'children': (4, 5, 6, 7)},
              {'type': 4, 'index': 43},
              {'type': 7, 'string': (44,)},
              {'type': 4, 'index': 43},
              {'type': 4, 'index': 11})},
 {'name': 'section-name',
  'lower': 'section-name',
  'index': 9,
  'line': 40,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 45},)},
 {'name': 'key-name',
  'lower': 'key-name',
  'index': 10,
  'line': 41,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 45},)},
 {'name': 'value',
  'lower': 'value',
  'index': 11,
  'line': 42,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3, 4, 5)},
              {'type': 4, 'index': 16},
              {'type': 4, 'index': 12},
              {'type': 4, 'index': 18},
              {'type': 4, 'index': 20},
              {'type': 4, 'index': 17})},
 {'name': 'boolean',
  'lower': 'boolean',
  'index': 12,
  'line': 43,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 4, 'index': 13},
              {'type': 4, 'index': 14},
              {'type': 4, 'index': 15})},
 {'name': 'true',
  'lower': 'true',
  'index': 13,
  'line': 44,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 7, 'string': (116, 114, 117, 101)},
              {'type': 7, 'string': (121, 101, 115)})},
 {'name': 'false',
  'lower': 'false',
  'index': 14,
  'line': 45,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 7, 'string': (102, 97, 108, 115, 101)},
              {'type': 7, 'string': (110, 111)})},
 {'name': 'null',
  'lower': 'null',
  'index': 15,
  'line': 46,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 7, 'string': (110, 117, 108, 108)},
              {'type': 7, 'string': (118, 111, 105, 100)})},
 {'name': 'number',
  'lower': 'number',
  'index': 16,
  'line': 47,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 4, 'index': 46})},
 {'name': 'string',
  'lower': 'string',
  'index': 17,
  'line': 48,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 8)},
              {'type': 1, 'children': (2, 3, 4, 5, 6, 7)},
              {'type': 6, 'string': (33,)},
              {'type': 5, 'min': 35, 'max': 38},
              {'type': 5, 'min': 40, 'max': 43},
              {'type': 5, 'min': 45, 'max': 91},
              {'type': 5, 'min': 93, 'max': 126},
              {'type': 4, 'index': 22},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (10, 11, 12, 13)},
              {'type': 5, 'min': 32, 'max': 43},
              {'type': 5, 'min': 45, 'max': 91},
              {'type': 5, 'min': 93, 'max': 126},
              {'type': 4, 'index': 22})},
 {'name': 'd-quoted-string',
  'lower': 'd-quoted-string',
  'index': 18,
  'line': 49,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3)},
              {'type': 6, 'string': (34,)},
              {'type': 4, 'index': 19},
              {'type': 6, 'string': (34,)})},
 {'name': 'd-quoted-value',
  'lower': 'd-quoted-value',
  'index': 19,
  'line': 50,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3, 4, 5)},
              {'type': 5, 'min': 32, 'max': 33},
              {'type': 5, 'min': 35, 'max': 91},
              {'type': 5, 'min': 93, 'max': 126},
              {'type': 4, 'index': 22})},
 {'name': 's-quoted-string',
  'lower': 's-quoted-string',
  'index': 20,
  'line': 51,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3)},
              {'type': 6, 'string': (39,)},
              {'type': 4, 'index': 21},
              {'type': 6, 'string': (39,)})},
 {'name': 's-quoted-value',
  'lower': 's-quoted-value',
  'index': 21,
  'line': 52,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3, 4, 5)},
              {'type': 5, 'min': 32, 'max': 38},
              {'type': 5, 'min': 40, 'max': 91},
              {'type': 5, 'min': 93, 'max': 126},
              {'type': 4, 'index': 22})},
 {'name': 'escaped',
  'lower': 'escaped',
  'index': 22,
  'line': 53,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (92,)},
              {'type': 1,
               'children': (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)},
              {'type': 4, 'index': 23},
              {'type': 4, 'index': 24},
              {'type': 4, 'index': 25},
              {'type': 4, 'index': 26},
              {'type': 4, 'index': 27},
              {'type': 4, 'index': 28},
              {'type': 4, 'index': 29},
              {'type': 4, 'index': 30},
              {'type': 4, 'index': 31},
              {'type': 4, 'index': 32},
              {'type': 4, 'index': 33},
              {'type': 4, 'index': 34},
              {'type': 4, 'index': 35},
              {'type': 4, 'index': 36})},
 {'name': 'back-slash',
  'lower': 'back-slash',
  'index': 23,
  'line': 67,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (92,)},)},
 {'name': 'double-quote',
  'lower': 'double-quote',
  'index': 24,
  'line': 68,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (34,)},)},
 {'name': 'hash',
  'lower': 'hash',
  'index': 25,
  'line': 69,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (35,)},)},
 {'name': 'single-quote',
  'lower': 'single-quote',
  'index': 26,
  'line': 70,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (39,)},)},
 {'name': 'comma',
  'lower': 'comma',
  'index': 27,
  'line': 71,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (44,)},)},
 {'name': 'colon',
  'lower': 'colon',
  'index': 28,
  'line': 72,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (58,)},)},
 {'name': 'semicolon',
  'lower': 'semicolon',
  'index': 29,
  'line': 73,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (59,)},)},
 {'name': 'equal-sign',
  'lower': 'equal-sign',
  'index': 30,
  'line': 74,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (61,)},)},
 {'name': 'blank',
  'lower': 'blank',
  'index': 31,
  'line': 75,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (98,)},)},
 {'name': 'tab',
  'lower': 'tab',
  'index': 32,
  'line': 76,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (116,)},)},
 {'name': 'line-feed',
  'lower': 'line-feed',
  'index': 33,
  'line': 77,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (110,)},)},
 {'name': 'carriage-return',
  'lower': 'carriage-return',
  'index': 34,
  'line': 78,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (114,)},)},
 {'name': 'unicode',
  'lower': 'unicode',
  'index': 35,
  'line': 79,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (117,)},
              {'type': 3, 'min': 4, 'max': 4},
              {'type': 4, 'index': 37})},
 {'name': 'hexadecimal',
  'lower': 'hexadecimal',
  'index': 36,
  'line': 80,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (120,)},
              {'type': 3, 'min': 2, 'max': 2},
              {'type': 4, 'index': 37})},
 {'name': 'hh',
  'lower': 'hh',
  'index': 37,
  'line': 81,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 5, 'min': 48, 'max': 57},
              {'type': 5, 'min': 65, 'max': 72},
              {'type': 5, 'min': 97, 'max': 104})},
 {'name': 'blank-line',
  'lower': 'blank-line',
  'index': 38,
  'line': 82,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 4, 'index': 39},
              {'type': 4, 'index': 40})},
 {'name': 'good-blank-line',
  'lower': 'good-blank-line',
  'index': 39,
  'line': 83,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 4)},
              {'type': 4, 'index': 43},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 42},
              {'type': 4, 'index': 41})},
 {'name': 'bad-blank-line',
  'lower': 'bad-blank-line',
  'index': 40,
  'line': 84,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 4, 5, 8, 10)},
              {'type': 1, 'children': (2, 3)},
              {'type': 6, 'string': (32,)},
              {'type': 6, 'string': (9,)},
              {'type': 4, 'index': 43},
              {'type': 1, 'children': (6, 7)},
              {'type': 5, 'min': 33, 'max': 58},
              {'type': 5, 'min': 60, 'max': 126},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 47},
              {'type': 4, 'index': 41})},
 {'name': 'line-end',
  'lower': 'line-end',
  'index': 41,
  'line': 85,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 6, 'string': (13, 10)},
              {'type': 6, 'string': (10,)},
              {'type': 6, 'string': (13,)})},
 {'name': 'comment',
  'lower': 'comment',
  'index': 42,
  'line': 86,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (59,)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 47})},
 {'name': 'wsp',
  'lower': 'wsp',
  'index': 43,
  'line': 87,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3)},
              {'type': 6, 'string': (32,)},
              {'type': 6, 'string': (9,)})},
 {'name': 'alpha',
  'lower': 'alpha',
  'index': 44,
  'line': 88,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 5, 'min': 65, 'max': 90},
              {'type': 5, 'min': 97, 'max': 122})},
 {'name': 'alphanum',
  'lower': 'alphanum',
  'index': 45,
  'line': 89,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 4)},
              {'type': 1, 'children': (2, 3)},
              {'type': 4, 'index': 44},
              {'type': 6, 'string': (95,)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (6, 7, 8)},
              {'type': 4, 'index': 44},
              {'type': 4, 'index': 46},
              {'type': 6, 'string': (95,)})},
 {'name': 'digit',
  'lower': 'digit',
  'index': 46,
  'line': 90,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 5, 'min': 48, 'max': 57},)},
 {'name': 'any',
  'lower': 'any',
  'index': 47,
  'line': 91,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 5, 'min': 32, 'max': 126},
              {'type': 6, 'string': (9,)})})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False


def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += ";\n"
    sabnf += "; Ref: https://en.wikipedia.org: INI File\n"
    sabnf += ";\n"
    sabnf += "; comments begin with the semicolon, \";\" and continue to the end of the line\n"
    sabnf += "; comments may appear on valid section and value lines as well as blank lines\n"
    sabnf += "; line ends may be CRLF, LF or CR\n"
    sabnf += "; tabs, 0x09, may NOT occur in quoted strings\n"
    sabnf += ";\n"
    sabnf += "; keys may have multiple values\n"
    sabnf += ";   - multiple values may be given as a comma delimited list on a single line\n"
    sabnf += ";   - multiple values may be listed separately on separate lines with the same key name\n"
    sabnf += ";\n"
    sabnf += "; section names are optional\n"
    sabnf += ";   - keys need not appear in a named section\n"
    sabnf += ";\n"
    sabnf += "; sections are \"disjoint\",\n"
    sabnf += ";   - that is the keys in multiple occurrences of a section name are\n"
    sabnf += ";   - simply joined together as if they appeared contiguously in a single section\n"
    sabnf += ";\n"
    sabnf += "; sections end at the beginning of a new section or the end of file\n"
    sabnf += ";\n"
    sabnf += "; section and key names are alphanumeric + underscore (must begin with alpha or underscore)\n"
    sabnf += "; values that are not alphanumeric must be single or double quoted\n"
    sabnf += ";\n"
    sabnf += "; The grammar is designed to accept any string of ASCII characters without failure.\n"
    sabnf += "; The \"error productions\", bad-section-line, bad-value-line, bad-blank-line are meant to accept all lines\n"
    sabnf += "; that are not otherwise correct blank, section or value lines. This is so that\n"
    sabnf += "; parser callback functions can recognize input errors and report or react to them\n"
    sabnf += "; in an application-dependent manner.\n"
    sabnf += ";\n"
    sabnf += ";\n"
    sabnf += "ini-file            = *(blank-line / value-line) *section\n"
    sabnf += "section             = section-line *(blank-line / value-line)\n"
    sabnf += "section-line        = good-section-line / bad-section-line\n"
    sabnf += "good-section-line   = \"[\" wsp section-name wsp \"]\" wsp [comment] line-end\n"
    sabnf += "bad-section-line    = \"[\" *any line-end;\n"
    sabnf += "value-line          = good-value / bad-value-line\n"
    sabnf += "good-value          = key-name wsp \"=\" wsp value-array wsp [comment] line-end\n"
    sabnf += "bad-value-line      = (%d33-90 / %d92-126) *any line-end\n"
    sabnf += "value-array         = value *(wsp \",\" wsp value)\n"
    sabnf += "section-name        = alphanum\n"
    sabnf += "key-name            = alphanum\n"
    sabnf += "value               = number / boolean / d-quoted-string / s-quoted-string / string\n"
    sabnf += "boolean             = true / false / null\n"
    sabnf += "true                = \"true\" / \"yes\"\n"
    sabnf += "false               = \"false\" / \"no\"\n"
    sabnf += "null                = \"null\" / \"void\"\n"
    sabnf += "number              = 1*digit\n"
    sabnf += "string              = (%d33 / %d35-38 / %d40-43 / %d45-91 / %d93-126 / escaped) *(%d32-43 / %d45-91 / %d93-126 / escaped)\n"
    sabnf += "d-quoted-string     = %d34  d-quoted-value %d34\n"
    sabnf += "d-quoted-value      = 1*(%d32-33 / %d35-91 / %d93-126 / escaped)\n"
    sabnf += "s-quoted-string     = %d39 s-quoted-value %d39\n"
    sabnf += "s-quoted-value      = 1*(%d32-38  /  %d40-91 / %d93-126 / escaped)\n"
    sabnf += "escaped             = %x5c (back-slash\n"
    sabnf += "                    / double-quote\n"
    sabnf += "                    / hash\n"
    sabnf += "                    / single-quote\n"
    sabnf += "                    / comma\n"
    sabnf += "                    / colon\n"
    sabnf += "                    / semicolon\n"
    sabnf += "                    / equal-sign\n"
    sabnf += "                    / blank\n"
    sabnf += "                    / tab\n"
    sabnf += "                    / line-feed\n"
    sabnf += "                    / carriage-return\n"
    sabnf += "                    / unicode\n"
    sabnf += "                    / hexadecimal)\n"
    sabnf += "back-slash          = %x5c\n"
    sabnf += "double-quote        = %x22\n"
    sabnf += "hash                = %x23\n"
    sabnf += "single-quote        = %x27\n"
    sabnf += "comma               = %x2c\n"
    sabnf += "colon               = %x3a\n"
    sabnf += "semicolon           = %x3b\n"
    sabnf += "equal-sign          = %x3d\n"
    sabnf += "blank               = %s\"b\"\n"
    sabnf += "tab                 = %s\"t\"\n"
    sabnf += "line-feed           = %s\"n\"\n"
    sabnf += "carriage-return     = %s\"r\"\n"
    sabnf += "unicode             = %s\"u\" 4hh\n"
    sabnf += "hexadecimal         = %s\"x\" 2hh\n"
    sabnf += "hh                  = %d48-57 / %d65-72 / %d97-104\n"
    sabnf += "blank-line          = good-blank-line / bad-blank-line\n"
    sabnf += "good-blank-line     = wsp [comment] line-end\n"
    sabnf += "bad-blank-line      = (%d32 / %d9) wsp (%d33-58 / %d60-126) *any line-end\n"
    sabnf += "line-end            = %d13.10 / %d10 / %d13\n"
    sabnf += "comment             = %d59 *any\n"
    sabnf += "wsp                 = *(%d32 / %d9)\n"
    sabnf += "alpha               = %d65-90 / %d97-122\n"
    sabnf += "alphanum            = (alpha / %d95) *(alpha / digit / %d95)\n"
    sabnf += "digit               = %d48-57\n"
    sabnf += "any                 = %d32-126 / %d9\n"
    return sabnf

