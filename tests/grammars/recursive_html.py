# Copyright (c) 2022 Lowell D. Thomas, all rights reserved
# BSD-2-Clause (https://opensource.org/licenses/BSD-2-Clause)
#

# SUMMARY
#      rules = 3
#       udts = 0
#    opcodes = 19
#        ---   ABNF original opcodes
#        ALT = 2
#        CAT = 2
#        REP = 2
#        RNM = 3
#        TLS = 4
#        TBS = 0
#        TRG = 5
#        ---   SABNF super set opcodes
#        UDT = 0
#        AND = 0
#        NOT = 0
#        BKA = 0
#        BKN = 0
#        BKR = 1
#        ABG = 0
#        AEN = 0
# characters = [47 - 122]
#

# RULES
rules = ({'name': 'HTML',
  'lower': 'html',
  'index': 0,
  'line': 0,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': True,
  'opcodes': ({'type': 2, 'children': (1, 2, 3, 4, 6, 7, 8)},
              {'type': 7, 'string': (60,)},
              {'type': 4, 'index': 1},
              {'type': 7, 'string': (62,)},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 4, 'index': 0},
              {'type': 7, 'string': (60, 47)},
              {'type': 14,
               'name': 'tag-name',
               'lower': 'tag-name',
               'bkr_case': 604,
               'bkr_mode': 602,
               'is_udt': False,
               'empty': None,
               'index': 1},
              {'type': 7, 'string': (62,)})},
 {'name': 'TAG-name',
  'lower': 'tag-name',
  'index': 1,
  'line': 1,
  'is_bkru': False,
  'is_bkrr': True,
  'has_bkrr': False,
  'opcodes': ({'type': 4, 'index': 2},)},
 {'name': 'alphanum',
  'lower': 'alphanum',
  'index': 2,
  'line': 2,
  'is_bkru': False,
  'is_bkrr': False,
  'has_bkrr': False,
  'opcodes': ({'type': 2, 'children': (1, 4)},
              {'type': 1, 'children': (2, 3)},
              {'type': 5, 'min': 97, 'max': 122},
              {'type': 5, 'min': 65, 'max': 90},
              {'type': 3, 'min': 0, 'max': 9223372036854775807},
              {'type': 1, 'children': (6, 7, 8)},
              {'type': 5, 'min': 97, 'max': 122},
              {'type': 5, 'min': 65, 'max': 90},
              {'type': 5, 'min': 48, 'max': 57})})

# UDTS
udts = ()

has_bkru = False
has_bkrr = True

def to_string():
    '''Displays the original SABNF syntax.'''
    sabnf = ""
    sabnf += "HTML     = \"<\" tag-name \">\" *HTML \"</\" \\%i%rtag-name \">\"\n"
    sabnf += "TAG-name = alphanum\n"
    sabnf += "alphanum = (%d97-122/%d65-90) *(%d97-122/%d65-90/%d48-57)\n"
    return sabnf

