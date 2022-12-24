# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 83
#       udts = 0
#    opcodes = 314
#        ---   ABNF original opcodes
#        ALT = 32
#        CAT = 43
#        REP = 27
#        RNM = 135
#        TLS = 0
#        TBS = 59
#        TRG = 18
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
rules = ({'name': 'file',
  'lower': 'file',
  'index': 0,
  'line': 56,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3)},
              {'type': 4, 'index': 1},
              {'type': 4, 'index': 2})},
 {'name': 'blank-line',
  'lower': 'blank-line',
  'index': 1,
  'line': 57,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 5, 7)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (3, 4)},
              {'type': 6, 'string': (32,)},
              {'type': 6, 'string': (9,)},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 80},
              {'type': 4, 'index': 81})},
 {'name': 'rule',
  'lower': 'rule',
  'index': 2,
  'line': 58,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4, 5)},
              {'type': 4, 'index': 3},
              {'type': 4, 'index': 77},
              {'type': 4, 'index': 8},
              {'type': 4, 'index': 77},
              {'type': 4, 'index': 81})},
 {'name': 'rule-lookup',
  'lower': 'rule-lookup',
  'index': 3,
  'line': 59,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3)},
              {'type': 4, 'index': 5},
              {'type': 4, 'index': 77},
              {'type': 4, 'index': 4})},
 {'name': 'equals',
  'lower': 'equals',
  'index': 4,
  'line': 60,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 4, 'index': 7},
              {'type': 4, 'index': 6})},
 {'name': 'rule-name',
  'lower': 'rule-name',
  'index': 5,
  'line': 61,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 76},)},
 {'name': 'defined',
  'lower': 'defined',
  'index': 6,
  'line': 62,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (61,)},)},
 {'name': 'inc-alt',
  'lower': 'inc-alt',
  'index': 7,
  'line': 63,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (61, 47)},)},
 {'name': 'alternation',
  'lower': 'alternation',
  'index': 8,
  'line': 64,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 9},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 2, 'children': (4, 5, 6)},
              {'type': 4, 'index': 77},
              {'type': 4, 'index': 34},
              {'type': 4, 'index': 9})},
 {'name': 'concatenation',
  'lower': 'concatenation',
  'index': 9,
  'line': 65,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 10},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 2, 'children': (4, 5)},
              {'type': 4, 'index': 35},
              {'type': 4, 'index': 10})},
 {'name': 'repetition',
  'lower': 'repetition',
  'index': 10,
  'line': 66,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 3)},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 11},
              {'type': 1, 'children': (4, 5, 6)},
              {'type': 4, 'index': 14},
              {'type': 4, 'index': 16},
              {'type': 4, 'index': 13})},
 {'name': 'modifier',
  'lower': 'modifier',
  'index': 11,
  'line': 67,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 5)},
              {'type': 2, 'children': (2, 3)},
              {'type': 4, 'index': 12},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 33},
              {'type': 4, 'index': 33})},
 {'name': 'predicate',
  'lower': 'predicate',
  'index': 12,
  'line': 69,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3, 4)},
              {'type': 4, 'index': 39},
              {'type': 4, 'index': 40},
              {'type': 4, 'index': 37},
              {'type': 4, 'index': 38})},
 {'name': 'element',
  'lower': 'element',
  'index': 13,
  'line': 73,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)},
              {'type': 4, 'index': 30},
              {'type': 4, 'index': 19},
              {'type': 4, 'index': 43},
              {'type': 4, 'index': 44},
              {'type': 4, 'index': 45},
              {'type': 4, 'index': 50},
              {'type': 4, 'index': 20},
              {'type': 4, 'index': 41},
              {'type': 4, 'index': 42},
              {'type': 4, 'index': 53})},
 {'name': 'group',
  'lower': 'group',
  'index': 14,
  'line': 83,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4)},
              {'type': 6, 'string': (40,)},
              {'type': 4, 'index': 77},
              {'type': 4, 'index': 8},
              {'type': 4, 'index': 15})},
 {'name': 'group-close',
  'lower': 'group-close',
  'index': 15,
  'line': 84,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 77},
              {'type': 6, 'string': (41,)})},
 {'name': 'option',
  'lower': 'option',
  'index': 16,
  'line': 85,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4)},
              {'type': 4, 'index': 17},
              {'type': 4, 'index': 77},
              {'type': 4, 'index': 8},
              {'type': 4, 'index': 18})},
 {'name': 'option-open',
  'lower': 'option-open',
  'index': 17,
  'line': 86,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (91,)},)},
 {'name': 'option-close',
  'lower': 'option-close',
  'index': 18,
  'line': 87,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 4, 'index': 77},
              {'type': 6, 'string': (93,)})},
 {'name': 'rnm-op',
  'lower': 'rnm-op',
  'index': 19,
  'line': 88,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 76},)},
 {'name': 'bkr-op',
  'lower': 'bkr-op',
  'index': 20,
  'line': 89,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 4)},
              {'type': 6, 'string': (92,)},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 4, 'index': 21},
              {'type': 4, 'index': 26})},
 {'name': 'bkrModifier',
  'lower': 'bkrmodifier',
  'index': 21,
  'line': 90,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 7, 13, 19)},
              {'type': 2, 'children': (2, 3)},
              {'type': 4, 'index': 22},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (5, 6)},
              {'type': 4, 'index': 24},
              {'type': 4, 'index': 25},
              {'type': 2, 'children': (8, 9)},
              {'type': 4, 'index': 23},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (11, 12)},
              {'type': 4, 'index': 24},
              {'type': 4, 'index': 25},
              {'type': 2, 'children': (14, 15)},
              {'type': 4, 'index': 24},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (17, 18)},
              {'type': 4, 'index': 22},
              {'type': 4, 'index': 23},
              {'type': 2, 'children': (20, 21)},
              {'type': 4, 'index': 25},
              {'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (23, 24)},
              {'type': 4, 'index': 22},
              {'type': 4, 'index': 23})},
 {'name': 'cs',
  'lower': 'cs',
  'index': 22,
  'line': 91,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (37, 115)},)},
 {'name': 'ci',
  'lower': 'ci',
  'index': 23,
  'line': 92,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (37, 105)},)},
 {'name': 'um',
  'lower': 'um',
  'index': 24,
  'line': 93,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (37, 117)},)},
 {'name': 'rm',
  'lower': 'rm',
  'index': 25,
  'line': 94,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (37, 114)},)},
 {'name': 'bkr-name',
  'lower': 'bkr-name',
  'index': 26,
  'line': 95,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 4, 'index': 28},
              {'type': 4, 'index': 29},
              {'type': 4, 'index': 27})},
 {'name': 'rname',
  'lower': 'rname',
  'index': 27,
  'line': 96,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 76},)},
 {'name': 'uname',
  'lower': 'uname',
  'index': 28,
  'line': 97,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (117, 95)},
              {'type': 4, 'index': 76})},
 {'name': 'ename',
  'lower': 'ename',
  'index': 29,
  'line': 98,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (101, 95)},
              {'type': 4, 'index': 76})},
 {'name': 'udt-op',
  'lower': 'udt-op',
  'index': 30,
  'line': 99,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 4, 'index': 32},
              {'type': 4, 'index': 31})},
 {'name': 'udt-non-empty',
  'lower': 'udt-non-empty',
  'index': 31,
  'line': 101,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (117, 95)},
              {'type': 4, 'index': 76})},
 {'name': 'udt-empty',
  'lower': 'udt-empty',
  'index': 32,
  'line': 102,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (101, 95)},
              {'type': 4, 'index': 76})},
 {'name': 'rep-op',
  'lower': 'rep-op',
  'index': 33,
  'line': 103,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 5, 8, 11, 12)},
              {'type': 2, 'children': (2, 3, 4)},
              {'type': 4, 'index': 57},
              {'type': 4, 'index': 36},
              {'type': 4, 'index': 59},
              {'type': 2, 'children': (6, 7)},
              {'type': 4, 'index': 57},
              {'type': 4, 'index': 36},
              {'type': 2, 'children': (9, 10)},
              {'type': 4, 'index': 36},
              {'type': 4, 'index': 59},
              {'type': 4, 'index': 36},
              {'type': 4, 'index': 58})},
 {'name': 'alt-op',
  'lower': 'alt-op',
  'index': 34,
  'line': 108,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (47,)},
              {'type': 4, 'index': 77})},
 {'name': 'cat-op',
  'lower': 'cat-op',
  'index': 35,
  'line': 109,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 78},)},
 {'name': 'star-op',
  'lower': 'star-op',
  'index': 36,
  'line': 110,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (42,)},)},
 {'name': 'and-op',
  'lower': 'and-op',
  'index': 37,
  'line': 111,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (38,)},)},
 {'name': 'not-op',
  'lower': 'not-op',
  'index': 38,
  'line': 112,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (33,)},)},
 {'name': 'bka-op',
  'lower': 'bka-op',
  'index': 39,
  'line': 113,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (38, 38)},)},
 {'name': 'bkn-op',
  'lower': 'bkn-op',
  'index': 40,
  'line': 114,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (33, 33)},)},
 {'name': 'abg-op',
  'lower': 'abg-op',
  'index': 41,
  'line': 115,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (37, 94)},)},
 {'name': 'aen-op',
  'lower': 'aen-op',
  'index': 42,
  'line': 116,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (37, 36)},)},
 {'name': 'trg-op',
  'lower': 'trg-op',
  'index': 43,
  'line': 117,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (37,)},
              {'type': 1, 'children': (3, 8, 13)},
              {'type': 2, 'children': (4, 5, 6, 7)},
              {'type': 4, 'index': 64},
              {'type': 4, 'index': 67},
              {'type': 6, 'string': (45,)},
              {'type': 4, 'index': 68},
              {'type': 2, 'children': (9, 10, 11, 12)},
              {'type': 4, 'index': 65},
              {'type': 4, 'index': 71},
              {'type': 6, 'string': (45,)},
              {'type': 4, 'index': 72},
              {'type': 2, 'children': (14, 15, 16, 17)},
              {'type': 4, 'index': 66},
              {'type': 4, 'index': 69},
              {'type': 6, 'string': (45,)},
              {'type': 4, 'index': 70})},
 {'name': 'tbs-op',
  'lower': 'tbs-op',
  'index': 44,
  'line': 120,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (37,)},
              {'type': 1, 'children': (3, 10, 17)},
              {'type': 2, 'children': (4, 5, 6)},
              {'type': 4, 'index': 64},
              {'type': 4, 'index': 61},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 2, 'children': (8, 9)},
              {'type': 6, 'string': (46,)},
              {'type': 4, 'index': 61},
              {'type': 2, 'children': (11, 12, 13)},
              {'type': 4, 'index': 65},
              {'type': 4, 'index': 62},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 2, 'children': (15, 16)},
              {'type': 6, 'string': (46,)},
              {'type': 4, 'index': 62},
              {'type': 2, 'children': (18, 19, 20)},
              {'type': 4, 'index': 66},
              {'type': 4, 'index': 63},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 2, 'children': (22, 23)},
              {'type': 6, 'string': (46,)},
              {'type': 4, 'index': 63})},
 {'name': 'tls-op',
  'lower': 'tls-op',
  'index': 45,
  'line': 123,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4)},
              {'type': 4, 'index': 46},
              {'type': 6, 'string': (34,)},
              {'type': 4, 'index': 48},
              {'type': 4, 'index': 47})},
 {'name': 'tls-case',
  'lower': 'tls-case',
  'index': 46,
  'line': 124,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 1},
              {'type': 1, 'children': (2, 3)},
              {'type': 4, 'index': 23},
              {'type': 4, 'index': 22})},
 {'name': 'tls-close',
  'lower': 'tls-close',
  'index': 47,
  'line': 125,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (34,)},)},
 {'name': 'tls-string',
  'lower': 'tls-string',
  'index': 48,
  'line': 126,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3, 4)},
              {'type': 5, 'min': 32, 'max': 33},
              {'type': 5, 'min': 35, 'max': 126},
              {'type': 4, 'index': 49})},
 {'name': 'string-tab',
  'lower': 'string-tab',
  'index': 49,
  'line': 127,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (9,)},)},
 {'name': 'cls-op',
  'lower': 'cls-op',
  'index': 50,
  'line': 128,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3)},
              {'type': 6, 'string': (39,)},
              {'type': 4, 'index': 52},
              {'type': 4, 'index': 51})},
 {'name': 'cls-close',
  'lower': 'cls-close',
  'index': 51,
  'line': 129,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (39,)},)},
 {'name': 'cls-string',
  'lower': 'cls-string',
  'index': 52,
  'line': 130,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3, 4)},
              {'type': 5, 'min': 32, 'max': 38},
              {'type': 5, 'min': 40, 'max': 126},
              {'type': 4, 'index': 49})},
 {'name': 'pros-val',
  'lower': 'pros-val',
  'index': 53,
  'line': 131,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2, 3)},
              {'type': 4, 'index': 54},
              {'type': 4, 'index': 55},
              {'type': 4, 'index': 56})},
 {'name': 'pros-val-open',
  'lower': 'pros-val-open',
  'index': 54,
  'line': 132,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (60,)},)},
 {'name': 'pros-val-string',
  'lower': 'pros-val-string',
  'index': 55,
  'line': 133,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3, 4)},
              {'type': 5, 'min': 32, 'max': 61},
              {'type': 5, 'min': 63, 'max': 126},
              {'type': 4, 'index': 49})},
 {'name': 'pros-val-close',
  'lower': 'pros-val-close',
  'index': 56,
  'line': 134,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 6, 'string': (62,)},)},
 {'name': 'rep-min',
  'lower': 'rep-min',
  'index': 57,
  'line': 135,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 60},)},
 {'name': 'rep-min-max',
  'lower': 'rep-min-max',
  'index': 58,
  'line': 136,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 60},)},
 {'name': 'rep-max',
  'lower': 'rep-max',
  'index': 59,
  'line': 137,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 60},)},
 {'name': 'rep-num',
  'lower': 'rep-num',
  'index': 60,
  'line': 138,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 5, 'min': 48, 'max': 57})},
 {'name': 'd-string',
  'lower': 'd-string',
  'index': 61,
  'line': 139,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 73},)},
 {'name': 'x-string',
  'lower': 'x-string',
  'index': 62,
  'line': 140,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 75},)},
 {'name': 'b-string',
  'lower': 'b-string',
  'index': 63,
  'line': 141,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 74},)},
 {'name': 'dec',
  'lower': 'dec',
  'index': 64,
  'line': 142,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 6, 'string': (68,)},
              {'type': 6, 'string': (100,)})},
 {'name': 'hex',
  'lower': 'hex',
  'index': 65,
  'line': 143,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 6, 'string': (88,)},
              {'type': 6, 'string': (120,)})},
 {'name': 'bin',
  'lower': 'bin',
  'index': 66,
  'line': 144,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2)},
              {'type': 6, 'string': (66,)},
              {'type': 6, 'string': (98,)})},
 {'name': 'dmin',
  'lower': 'dmin',
  'index': 67,
  'line': 145,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 73},)},
 {'name': 'dmax',
  'lower': 'dmax',
  'index': 68,
  'line': 146,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 73},)},
 {'name': 'bmin',
  'lower': 'bmin',
  'index': 69,
  'line': 147,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 74},)},
 {'name': 'bmax',
  'lower': 'bmax',
  'index': 70,
  'line': 148,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 74},)},
 {'name': 'xmin',
  'lower': 'xmin',
  'index': 71,
  'line': 149,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 75},)},
 {'name': 'xmax',
  'lower': 'xmax',
  'index': 72,
  'line': 150,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 75},)},
 {'name': 'dnum',
  'lower': 'dnum',
  'index': 73,
  'line': 151,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 5, 'min': 48, 'max': 57})},
 {'name': 'bnum',
  'lower': 'bnum',
  'index': 74,
  'line': 152,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 5, 'min': 48, 'max': 49})},
 {'name': 'xnum',
  'lower': 'xnum',
  'index': 75,
  'line': 153,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 1, 'children': (2, 3, 4)},
              {'type': 5, 'min': 48, 'max': 57},
              {'type': 5, 'min': 65, 'max': 70},
              {'type': 5, 'min': 97, 'max': 102})},
 {'name': 'alphanum',
  'lower': 'alphanum',
  'index': 76,
  'line': 156,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 4)},
              {'type': 1, 'children': (2, 3)},
              {'type': 5, 'min': 97, 'max': 122},
              {'type': 5, 'min': 65, 'max': 90},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (6, 7, 8, 9)},
              {'type': 5, 'min': 97, 'max': 122},
              {'type': 5, 'min': 65, 'max': 90},
              {'type': 5, 'min': 48, 'max': 57},
              {'type': 6, 'string': (45,)})},
 {'name': 'owsp',
  'lower': 'owsp',
  'index': 77,
  'line': 157,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 79})},
 {'name': 'wsp',
  'lower': 'wsp',
  'index': 78,
  'line': 158,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 3, 'min': 1, 'max': 9223372036854775807},
              {'type': 4, 'index': 79})},
 {'name': 'space',
  'lower': 'space',
  'index': 79,
  'line': 159,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3, 4)},
              {'type': 6, 'string': (32,)},
              {'type': 6, 'string': (9,)},
              {'type': 4, 'index': 80},
              {'type': 4, 'index': 82})},
 {'name': 'comment',
  'lower': 'comment',
  'index': 80,
  'line': 163,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 2)},
              {'type': 6, 'string': (59,)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (4, 5)},
              {'type': 5, 'min': 32, 'max': 126},
              {'type': 6, 'string': (9,)})},
 {'name': 'line-end',
  'lower': 'line-end',
  'index': 81,
  'line': 164,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 1, 'children': (1, 2, 3)},
              {'type': 6, 'string': (13, 10)},
              {'type': 6, 'string': (10,)},
              {'type': 6, 'string': (13,)})},
 {'name': 'line-continue',
  'lower': 'line-continue',
  'index': 82,
  'line': 167,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 5)},
              {'type': 1, 'children': (2, 3, 4)},
              {'type': 6, 'string': (13, 10)},
              {'type': 6, 'string': (10,)},
              {'type': 6, 'string': (13,)},
              {'type': 1, 'children': (6, 7)},
              {'type': 6, 'string': (32,)},
              {'type': 6, 'string': (9,)})})

# UDTS
udts = ()

has_bkru = False
has_bkrr = False


def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += ";\n"
    sabnf += "; ABNF for Python APG SABNF\n"
    sabnf += "; 08/19/2022\n"
    sabnf += "; RFC 5234 with some restrictions and additions.\n"
    sabnf += "; Compliant with  RFC 7405 for case-sensitive literal string notation\n"
    sabnf += ";  - accepts %s\"string\" as a case-sensitive string\n"
    sabnf += ";  - accepts %i\"string\" as a case-insensitive string\n"
    sabnf += ";  - accepts \"string\" as a case-insensitive string\n"
    sabnf += ";  - accepts 'string' as a case-sensitive string\n"
    sabnf += ";\n"
    sabnf += "; Some restrictions:\n"
    sabnf += ";   1. Rules must begin at first character of each line.\n"
    sabnf += ";      Indentations on first rule and rules thereafter are not allowed.\n"
    sabnf += ";   2. Relaxed line endings. CRLF, LF or CR are accepted as valid line ending.\n"
    sabnf += ";   3. Prose values, i.e. <prose value>, are accepted as valid grammar syntax.\n"
    sabnf += ";      However, a working parser cannot be generated from them.\n"
    sabnf += ";\n"
    sabnf += "; Super set (SABNF) additions:\n"
    sabnf += ";   1. Look-ahead (syntactic predicate) operators are accepted as element prefixes.\n"
    sabnf += ";      & is the positive look-ahead operator, succeeds and backtracks if the look-ahead phrase is found\n"
    sabnf += ";      ! is the negative look-ahead operator, succeeds and backtracks if the look-ahead phrase is NOT found\n"
    sabnf += ";      e.g. &%d13 or &rule or !(A / B)\n"
    sabnf += ";   2. User-defined Terminals (UDT) of the form, u_name and e_name are accepted.\n"
    sabnf += ";      They indicate the the user will hand-write the phrase acceptance algorithm.\n"
    sabnf += ";      e_name may return an empty phrase.\n"
    sabnf += ";      u_name may not return an empty phrase. The parser will inforce this.\n"
    sabnf += ";      'name' is alpha followed by alpha/num/hyphen just like a rule name.\n"
    sabnf += ";      u_name/e_name may be used as an element but no rule definition is given.\n"
    sabnf += ";      e.g. rule = A / u_myUdt\n"
    sabnf += ";           A = \"a\"\n"
    sabnf += ";      would be a valid grammar.\n"
    sabnf += ";      e_name \n"
    sabnf += ";   3. Case-sensitive, single-quoted strings are accepted.\n"
    sabnf += ";      e.g. 'abc' would be equivalent to %d97.98.99\n"
    sabnf += ";      (kept for backward compatibility, but superseded by %s\"abc\")  \n"
    sabnf += ";   4. Look-behind operators are accepted as element prefixes.\n"
    sabnf += ";      && is the positive look-behind operator, succeeds and backtracks if the look-behind phrase is found\n"
    sabnf += ";      !! is the negative look-behind operator, succeeds and backtracks if the look-behind phrase is NOT found\n"
    sabnf += ";      e.g. &&%d13 or &&rule or !!(A / B)\n"
    sabnf += ";   5. Back referencing operators, i.e. \\rulename or \\e_name or \\u_name, are accepted.\n"
    sabnf += ";      A back reference operator acts like a TLS or TBS terminal except that the phrase it attempts\n"
    sabnf += ";      to match is a phrase previously matched by the rule or UDT 'rulename', 'e_name' or 'u_name'.\n"
    sabnf += ";      There are two modes of previous phrase matching - the recursive mode and the universal mode.\n"
    sabnf += ";      In universal mode, \\rulename matches the last match to 'rulename' regardless of where it was found.\n"
    sabnf += ";      In recursive mode, \\rulename matches the last match found on the closest recursive parent.\n"
    sabnf += ";      It would be used primarily with \"nesting pairs\" type recursive rules.\n"
    sabnf += ";      Back reference modifiers can be used to specify case and mode.\n"
    sabnf += ";      \\A defaults to case-insensitive and universal mode, e.g. \\A === \\%i%uA\n"
    sabnf += ";      Modifiers %i and %s determine case-insensitive and case-sensitive mode, respectively.\n"
    sabnf += ";      Modifiers %u and %r determine universal mode and recursive mode, respectively.\n"
    sabnf += ";      Case and mode modifiers can appear in any order, e.g. \\%s%rA === \\%r%sA. \n"
    sabnf += ";   7. String begin anchor, ABG(%^) matches the beginning of the input string location.\n"
    sabnf += ";      Returns EMPTY or NOMATCH. Never consumes any characters.\n"
    sabnf += ";   8. String end anchor, AEN(%$) matches the end of the input string location.\n"
    sabnf += ";      Returns EMPTY or NOMATCH. Never consumes any characters.\n"
    sabnf += ";\n"
    sabnf += "file                = *(blank-line / rule)\n"
    sabnf += "blank-line          = *(%d32/%d9) [comment] line-end\n"
    sabnf += "rule                = rule-lookup owsp alternation owsp line-end\n"
    sabnf += "rule-lookup         = (rule-name) owsp equals\n"
    sabnf += "equals              = inc-alt / defined\n"
    sabnf += "rule-name           = alphanum\n"
    sabnf += "defined             = %d61\n"
    sabnf += "inc-alt             = %d61.47\n"
    sabnf += "alternation         = concatenation *(owsp alt-op concatenation)\n"
    sabnf += "concatenation       = repetition *(cat-op repetition)\n"
    sabnf += "repetition          = [modifier] (group / option / element)\n"
    sabnf += "modifier            = (predicate [rep-op])\n"
    sabnf += "                    / rep-op\n"
    sabnf += "predicate           = bka-op\n"
    sabnf += "                    / bkn-op\n"
    sabnf += "                    / and-op\n"
    sabnf += "                    / not-op\n"
    sabnf += "element             = udt-op\n"
    sabnf += "                    / rnm-op\n"
    sabnf += "                    / trg-op\n"
    sabnf += "                    / tbs-op\n"
    sabnf += "                    / tls-op\n"
    sabnf += "                    / cls-op\n"
    sabnf += "                    / bkr-op\n"
    sabnf += "                    / abg-op\n"
    sabnf += "                    / aen-op\n"
    sabnf += "                    / pros-val\n"
    sabnf += "group               = %d40 owsp  alternation group-close\n"
    sabnf += "group-close         = owsp %d41\n"
    sabnf += "option              = option-open owsp alternation option-close\n"
    sabnf += "option-open         = %d91\n"
    sabnf += "option-close        = owsp %d93\n"
    sabnf += "rnm-op              = alphanum\n"
    sabnf += "bkr-op              = %d92 [bkrModifier] bkr-name\n"
    sabnf += "bkrModifier         = (cs [um / rm]) / (ci [um / rm]) / (um [cs /ci]) / (rm [cs / ci])\n"
    sabnf += "cs                  = '%s'\n"
    sabnf += "ci                  = '%i'\n"
    sabnf += "um                  = '%u'\n"
    sabnf += "rm                  = '%r'\n"
    sabnf += "bkr-name            = uname / ename / rname\n"
    sabnf += "rname               = alphanum\n"
    sabnf += "uname               = %d117.95 alphanum\n"
    sabnf += "ename               = %d101.95 alphanum\n"
    sabnf += "udt-op              = udt-empty\n"
    sabnf += "                    / udt-non-empty\n"
    sabnf += "udt-non-empty       = %d117.95 alphanum\n"
    sabnf += "udt-empty           = %d101.95 alphanum\n"
    sabnf += "rep-op              = (rep-min star-op rep-max)\n"
    sabnf += "                    / (rep-min star-op)\n"
    sabnf += "                    / (star-op rep-max)\n"
    sabnf += "                    / star-op\n"
    sabnf += "                    / rep-min-max\n"
    sabnf += "alt-op              = %d47 owsp\n"
    sabnf += "cat-op              = wsp\n"
    sabnf += "star-op             = %d42\n"
    sabnf += "and-op              = %d38\n"
    sabnf += "not-op              = %d33\n"
    sabnf += "bka-op              = %d38.38\n"
    sabnf += "bkn-op              = %d33.33\n"
    sabnf += "abg-op              = %d37.94\n"
    sabnf += "aen-op              = %d37.36\n"
    sabnf += "trg-op              = %d37 ((dec dmin %d45 dmax) \n"
    sabnf += "                    / (hex xmin %d45 xmax) \n"
    sabnf += "                    / (bin bmin %d45 bmax))\n"
    sabnf += "tbs-op              = %d37 ((dec d-string *(%d46 d-string)) \n"
    sabnf += "                    / (hex x-string *(%d46 x-string)) \n"
    sabnf += "                    / (bin b-string *(%d46 b-string)))\n"
    sabnf += "tls-op              = tls-case %d34 tls-string tls-close\n"
    sabnf += "tls-case            = [ci / cs]\n"
    sabnf += "tls-close           = %d34\n"
    sabnf += "tls-string          = *(%d32-33/%d35-126/string-tab)\n"
    sabnf += "string-tab          = %d9\n"
    sabnf += "cls-op              = %d39 cls-string cls-close\n"
    sabnf += "cls-close           = %d39\n"
    sabnf += "cls-string          = *(%d32-38/%d40-126/string-tab)\n"
    sabnf += "pros-val            = pros-val-open pros-val-string pros-val-close\n"
    sabnf += "pros-val-open       = %d60\n"
    sabnf += "pros-val-string     = *(%d32-61/%d63-126/string-tab)\n"
    sabnf += "pros-val-close      = %d62\n"
    sabnf += "rep-min             = rep-num\n"
    sabnf += "rep-min-max         = rep-num\n"
    sabnf += "rep-max             = rep-num\n"
    sabnf += "rep-num             = 1*(%d48-57)\n"
    sabnf += "d-string            = dnum\n"
    sabnf += "x-string            = xnum\n"
    sabnf += "b-string            = bnum\n"
    sabnf += "dec                 = (%d68/%d100)\n"
    sabnf += "hex                 = (%d88/%d120)\n"
    sabnf += "bin                 = (%d66/%d98)\n"
    sabnf += "dmin                = dnum\n"
    sabnf += "dmax                = dnum\n"
    sabnf += "bmin                = bnum\n"
    sabnf += "bmax                = bnum\n"
    sabnf += "xmin                = xnum\n"
    sabnf += "xmax                = xnum\n"
    sabnf += "dnum                = 1*(%d48-57)\n"
    sabnf += "bnum                = 1*%d48-49\n"
    sabnf += "xnum                = 1*(%d48-57 / %d65-70 / %d97-102)\n"
    sabnf += ";\n"
    sabnf += "; Basics\n"
    sabnf += "alphanum            = (%d97-122/%d65-90) *(%d97-122/%d65-90/%d48-57/%d45)\n"
    sabnf += "owsp                = *space\n"
    sabnf += "wsp                 = 1*space\n"
    sabnf += "space               = %d32\n"
    sabnf += "                    / %d9\n"
    sabnf += "                    / comment\n"
    sabnf += "                    / line-continue\n"
    sabnf += "comment             = %d59 *(%d32-126 / %d9)\n"
    sabnf += "line-end            = %d13.10\n"
    sabnf += "                    / %d10\n"
    sabnf += "                    / %d13\n"
    sabnf += "line-continue       = (%d13.10 / %d10 / %d13) (%d32 / %d9)\n"
    return sabnf

