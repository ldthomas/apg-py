''' @file apg_py/api/api.py
@brief An API for generating grammar objects from SABNF grammars.
@dir apg_py All of the APG library, generator and pattern-matching files.
@dir apg_py/api The parser generator files.
@dir apg_py/exp The pattern-matching files.
@dir apg_py/lib The basic APG parsing library.
@dir docs Documentation helper files for [doxygen](https://www.doxygen.nl/).
'''
from apg_py.api import sabnf_grammar
from apg_py.lib.parser import Parser
from apg_py.lib.ast import Ast
from apg_py.lib import identifiers as id
from apg_py.api.scanner import scanner
from apg_py.api.syntax import syntax
from apg_py.api.semantic import semantic
# from apg.api.attributes import attributes
from apg_py.api.rule_dependencies import display_deps, rule_dependencies
from apg_py.api.rule_attributes import display_rule_attributes, rule_attributes
from apg_py.api.syntax_callbacks import add_syntax_callbacks
from apg_py.api.semantic_callbacks import add_ast_callbacks
from apg_py.lib.utilities import tuple_to_ascii
from apg_py.lib.utilities import tuple_to_ascii_underline
from apg_py.lib.utilities import string_to_tuple
from pprint import pprint
import sys


class Grammar():
    '''Creates a grammar object which can be used by the APG library.
    '''

    def __init__(self, rules, udts, source):
        '''Grammar constructor.
        @param rules The generated rules list from Api.generate().
        @param udts The generated UDT list from Api.generate().
        @param source The original SABNF syntax source.
        '''
        self.has_bkru = False
        self.has_bkrr = False
        for rule in rules:
            for op in rule['opcodes']:
                if(op['type'] == id.ALT or op['type'] == id.CAT):
                    op['children'] = tuple(op['children'])
            if(op['type'] == id.TBS or op['type'] == id.TLS):
                op['string'] = tuple(op['string'])
            rule['opcodes'] = tuple(rule['opcodes'])
            if(rule['is_bkru']):
                self.has_bkru = True
            if(rule['is_bkrr']):
                self.has_bkrr = True
        for udt in udts:
            if(udt['is_bkru']):
                self.has_bkru = True
            if(udt['is_bkrr']):
                self.has_bkrr = True
        self.rules = tuple(rules)
        self.udts = tuple(udts)
        self.source = source


class Api():
    '''The API class. Houses all of the facilities needed to
    process an SABNF grammar syntax
    into a grammar object that can be used by an APG parser.'''

    class NameList():
        '''A helper class to keep track of rule and UDT names.
        Maintains a list of rule/UDT names, the lower case for easy
        comparisons and the rule/UDT index for the name.
        '''

        def __init__(self):
            self.names = []

        def add(self, name):
            '''Add a name to the list.
            @param name The name to add.
            @returns Returns the saved dictionary with the name,
            lower case name and the matching index.
            Returns -1 if the name already exists in the list.
            '''
            ret = -1
            find = self.get(name)
            if(find == -1):
                # name does not exist in list so add it
                ret = {
                    'name': name,
                    'lower': name.lower(),
                    'index': len(
                        self.names)}
                self.names.append(ret)
            # else: name already exists, -1 return indicates duplicate names
            return ret

        def get(self, name):
            '''Retrieve a name from the list.
            @param name The name to retrieve.
            @returns Returns the saved dictionary if the name is in the list.
            Returns -1 if the name does not exist in the list.
            '''
            ret = -1
            lower = name.lower()
            for n in self.names:
                if(n['lower'] == lower):
                    ret = n
                    break
            return ret

    def __init__(self):
        '''API constructor.
        self.errors is a list of errors. Each item, error, contains:
          - error['line'] - The line number(zero-based) where
            the error occurred.
          - error['index'] - The character index where the error occurred.
          - error['msg'] - A text message describing the error.

        self.lines is a list of the text lines in the input grammar.
        Each item, line, contains:
          - line['line_no'] - The zero-based line number.
          - line['index'] - The offset to the first character of the line.
          - line['length'] - The number of characters in the line,
            including the line end characters, if any.
          - line['text_length'] - the number of characters in the line,
            not including the line end characters.
          - line['end'] - Designates the line end characters.
            - 'CRLF' - Carriage return, line feed pair (\\r\\n or 0x0D0A)
            - 'CR' - Carriage return only (\\r or 0x0D)
            - 'LF' - Line feed only (\\n or 0x0A)
            - '' - Empty string means no line end at all
               (possible for last line.)
        '''
        self.parser = Parser(sabnf_grammar)
        self.ast = Ast(self.parser)
        add_syntax_callbacks(self.parser)
        add_ast_callbacks(self.ast)
        # place holders
        self.errors = None
        self.lines = None
        self.grammar = None
        self.source = None
        self.input = None
        self.rules = None
        self.udts = None
        self.rule_names = None
        self.udt_names = None
        self.rule_deps = None

    def generate(self, source, strict=False, phase='all'):
        '''Generate a grammar object from an SABNF grammar syntax.
        Works its way through multiple steps.
            - scan source for invalid characters, catalog lines
            - parse the source, syntax check
            - translate the parsed AST, semantic check
            - attributes (left recursion, etc.) and rule dependencies
            - construct the grammar object
        @param source An SABNF grammar syntax as a Python string.
        @param strict If True, source must be constrained to strictly follow
        the ABNF conventions of RFCs 5234 & 7405. If False, SABNF operators
        and line ending conventions are followed.
        @param phase Used primarily for debugging.
            - 'scanner' - generation halts after the scanner phase
            - 'syntax' - generation halts after the syntax phase
            - 'semantic' - generation halts after the semantic phase
            - 'attributes' - generation halts after the attributes phase
            - 'all' - (default) a grammar object is generated if no errors
             in any phases
        @return If successful, returns the grammar object.
        Otherwise, returns None. Use, for example<br>
        <pre>
        grammar = api.generator(...)
        if(not grammar):
            if(api.errors):
                print(api.display_errors())
            raise Exception('api.generate() failed')
        # use the generated grammar
        </pre>
        '''

        def discover_has_bkrr(rules, udts, rule_deps):
            '''Discover which rules reference rules which are
            recursive backreferenced.'''
            rule_range = range(len(rules))
            udt_range = range(len(udts))
            for i in rule_range:
                rdi = rule_deps[i]
                rules[i]['has_bkrr'] = False
                if(rdi['recursive_type'] != id.ATTR_N):
                    for j in rule_range:
                        if(rdi['refers_to'][j]):
                            if(rules[j]['is_bkrr']):
                                rules[i]['has_bkrr'] = True
                    for j in udt_range:
                        if(rdi['refers_to_udt'][j]):
                            if(udts[j]['is_bkrr']):
                                rules[i]['has_bkrr'] = True

        # scan for bad characters and generate a line catalog
        self.source = source
        self.input = string_to_tuple(self.source)
        result = scanner(self.input, strict)
        self.errors = result['errors']
        self.lines = result['lines']
        if(len(self.errors)):
            return
        if(phase == 'scanner'):
            return

        # syntax - check for SABNF syntax errors
        self.errors = syntax(self, strict)
        if(len(self.errors)):
            return
        if(phase == 'syntax'):
            return

        # semantic - check for SABNF semantic errors
        result = semantic(self)
        self.errors = result['errors']
        if(len(self.errors)):
            return
        self.rules = result['rules']
        self.udts = result['udts']
        self.rule_names = result['rule_names']
        self.udt_names = result['udt_names']
        if(phase == 'semantic'):
            return

        # discover all rule dependencies, including mutually-recursive groups
        self.rule_deps = rule_dependencies(
            self.rules,
            self.udts,
            self.rule_names,
            self.udt_names)

        # discover which recursive rules refer to back referenced rules
        discover_has_bkrr(self.rules, self.udts, self.rule_deps)

        # discover all rule attributes, reporting attribute errors
        result = rule_attributes(self.rules, self.rule_deps)
        self.errors = result['errors']
        self.attributes = result['attributes']
        if(len(self.errors)):
            return
        if(phase == 'attributes'):
            return

        # return the grammar object
        self.grammar = Grammar(self.rules, self.udts, self.source)
        return Grammar(self.rules, self.udts, self.source)

    def write_grammar(self, fname):
        '''Write the APG grammar to a file in format for later use by a parser.
        @param fname the file name to write the grammar to
        '''
        def grammar_copyright():
            display = ''
            display += '# Copyright (c) 2022 Lowell D. Thomas, '
            display += 'all rights reserved\n'
            display += '# BSD-2-Clause '
            display += '(https://opensource.org/licenses/BSD-2-Clause)\n'
            display += '#\n'
            return display

        def grammar_summary(rules, udts):
            def inc_op(op):
                op_id = op['type']
                info['op_counts'][op_id] += 1
                if(op_id == id.TLS or op_id == id.TBS):
                    for ch in op['string']:
                        if(ch < info['char_min']):
                            info['char_min'] = ch
                        if(ch > info['char_max']):
                            info['char_max'] = ch
                if(op_id == id.TRG):
                    if(op['min'] < info['char_min']):
                        info['char_min'] = op['min']
                    if(op['max'] > info['char_max']):
                        info['char_max'] = op['max']

            info = {'op_counts': [0] * (id.AEN + 1),
                    'opcodes': 0,
                    'char_min': sys.maxsize,
                    'char_max': 0}
            rule_count = len(rules)
            udt_count = len(udts)

            for rule in rules:
                info['opcodes'] += len(rule['opcodes'])
                for op in rule['opcodes']:
                    inc_op(op)

            display = '# SUMMARY'
            display += '\n#      rules = ' + str(rule_count)
            display += '\n#       udts = ' + str(udt_count)
            display += '\n#    opcodes = ' + str(info['opcodes'])
            display += '\n#        ---   ABNF original opcodes'
            display += '\n#        ALT = ' + str(info['op_counts'][id.ALT])
            display += '\n#        CAT = ' + str(info['op_counts'][id.CAT])
            display += '\n#        REP = ' + str(info['op_counts'][id.REP])
            display += '\n#        RNM = ' + str(info['op_counts'][id.RNM])
            display += '\n#        TLS = ' + str(info['op_counts'][id.TLS])
            display += '\n#        TBS = ' + str(info['op_counts'][id.TBS])
            display += '\n#        TRG = ' + str(info['op_counts'][id.TRG])
            display += '\n#        ---   SABNF super set opcodes'
            display += '\n#        UDT = ' + str(info['op_counts'][id.UDT])
            display += '\n#        AND = ' + str(info['op_counts'][id.AND])
            display += '\n#        NOT = ' + str(info['op_counts'][id.NOT])
            display += '\n#        BKA = ' + str(info['op_counts'][id.BKA])
            display += '\n#        BKN = ' + str(info['op_counts'][id.BKN])
            display += '\n#        BKR = ' + str(info['op_counts'][id.BKR])
            display += '\n#        ABG = ' + str(info['op_counts'][id.ABG])
            display += '\n#        AEN = ' + str(info['op_counts'][id.AEN])
            display += '\n# characters = ['
            display += str(info['char_min'])
            display += ' - '
            display += str(info['char_max'])
            display += ']'
            if(udt_count):
                display += ' + user defined'
            display += '\n#\n'
            return display

        def grammar_to_string(lines, source):
            display = 'def to_string():\n'
            display += "    '''Displays the original SABNF syntax.'''\n"
            display += '    sabnf = ""\n'
            for line in lines:
                display += '    sabnf += "'
                for i in range(line['index'], line['index'] + line['length']):
                    ch = ord(source[i])
                    if(ch == 9):
                        display += " "
                    elif(ch == 10):
                        display += "\\n"
                    elif(ch == 13):
                        display += "\\r"
                    elif(ch == 34):
                        display += '\\"'
                    elif(ch == 92):
                        display += "\\\\"
                    else:
                        display += source[i]
                display += '"\n'
            display += '    return sabnf\n'
            return display

        if(not self.grammar):
            raise Exception('no grammar has been generated')
        stdout_save = sys.stdout
        try:
            sys.stdout = open(fname, 'w')
            print(grammar_copyright())
            print(grammar_summary(self.grammar.rules, self.grammar.udts))
            print('# RULES')
            print('rules = ', end='')
            pprint(self.grammar.rules, sort_dicts=False)
            print()
            print('# UDTS')
            print('udts = ', end='')
            pprint(self.grammar.udts, sort_dicts=False)
            print()
            print('has_bkru = ', end='')
            print(self.grammar.has_bkru)
            print('has_bkrr = ', end='')
            print(self.grammar.has_bkrr)
            print()
            print()
            print(grammar_to_string(self.lines, self.grammar.source))
            sys.stdout.close()
        finally:
            sys.stdout = stdout_save

    def display_rule_attributes(self, sort='index'):
        '''Display the rule attributes.
        @param sort Determines the order of rule display.
            - 'index' (default) rules are listed in the order they appear
            in the grammar
            - 'type' rules are listed by recursive type
        @returns Returns a string with the displayed rule attributes.
        '''
        if(sort != 'index'):
            sort = 'type'
        if(self.attributes):
            return display_rule_attributes(self.attributes, sort)
        return 'rule attributes not available'

    def display_rule_dependencies(self, sort='index'):
        '''Display the rule dependencies. For each rule R, list both
        the list of rules that R refers to (both directly and indirectly)
        and the list of rules that refer to R (both directly and indirectly).
        @param sort Determines the order of display of the rules, R.
            - 'index' (default) rules are listed in the order they appear
            in the grammar
            - 'alpha' (actually anything but 'index') rules are listed
            alphabetically
        @returns Returns a string with the displayed rule dependencies.
        '''
        alpha = sort == 'index'
        if(self.rule_deps):
            return display_deps(
                self.rule_deps,
                self.rules,
                self.udts,
                alpha)
        return 'rule dependencies not available'

    def find_line(self, index):
        '''Find the line number of the line in which the given
        character occurs.
        @param index The (zero-based) index of the character in the source.
        @returns Returns the line number of the specified character.
        If index is out of range, returns the last line.'''
        if(len(self.lines) == 0):
            raise Exception(
                'find_line: No lines - no input (source grammar) defined.')
        if(index <= 0):
            return 0
        if(index >= len(self.input)):
            return len(self.lines) - 1
        line_no = -1
        for line in self.lines:
            line_no += 1
            if(index >= line['index'] and
               index < line['index'] + line['length']):
                return line_no
        raise Exception('find_line: Should never reach here - internal error.')

    def display_errors(self):
        '''Display the list of SABNF errors, if any.
        For each error, lists the line number and relative character offset
        where the error occurred and a descriptive message.
        @returns Returns a string of the displayed error messages.'''
        if(len(self.errors) == 0):
            return 'no errors'
        display = ''
        for error in self.errors:
            offset = error['index'] - self.lines[error['line']]['index']
            if(offset < 0):
                offset = 0
            display += self.display_underline(error['line'], offset)
            display += '\n'
            display += ('line: %d: offset: %d: %s' %
                        (error['line'], offset, error['msg']))
            display += '\n'
        return display

    def display_grammar(self):
        '''Displays an annotated version of the SABNF grammar syntax.
        Each line is preceeded by the line number and character offset
        of the line.
        @returns Returns a string of the display text.'''
        display = ''
        no = 0
        source = string_to_tuple(self.source)
        for line in self.lines:
            last_index = line['index'] + line['length']
            text = tuple_to_ascii(source[line['index']: last_index])
            display += ('%03d: %03d: %s' % (no, line['index'], text))
            display += '\n'
            no += 1
        return display

    def display_line(self, line_no):
        '''Displays a line with special characters accounted for.
        @param line_no The line number to display
        @returns Returns a string of the displayed line.'''
        if(line_no >= 0 and line_no < len(self.lines)):
            line = self.lines[line_no]
            last_index = line['index'] + line['length']
            return tuple_to_ascii(self.input[line['index']:last_index])
        return 'line_no ' + str(line_no) + ' out of range'

    def display_underline(self, line_no, index):
        '''Displays a syntax line, underlined with carrets highlightling
         error locations.
        @param line_no The line number to display
        @param index The index of the character to highlight
        @returns Returns a string of the displayed line.
        '''
        if(line_no >= 0 and line_no < len(self.lines)):
            map = []
            line = self.lines[line_no]
            last_index = line['index'] + line['length']
            line_segment = self.input[line['index']:last_index]
            text = tuple_to_ascii(line_segment, map)
            text += '\n'
            text += tuple_to_ascii_underline(map, index)
            return text
        return 'line_no ' + str(line_no) + ' out of range'

    def display_rules(self, sort='index'):
        '''Display the syntax rules and UDTs, if available.
        @param sort
          - 'index'(default) - display rules in the order
          in which they are defined
          - 'alpha' - display rules alphabetically
        '''
        def sort_rules_alpha(val):
            return self.rules[val]['lower']

        def sort_udts_alpha(val):
            return self.udts[val]['lower']

        display = ''
        if(self.rules):
            rule_count = len(self.rules)
            rule_range = range(rule_count)
            udt_count = len(self.udts)
            udt_range = range(udt_count)
            irules = [0] * rule_count
            iudts = [0] * udt_count
            for i in rule_range:
                irules[i] = i
            for i in udt_range:
                iudts[i] = i
            if(sort == 'alpha'):
                irules.sort(key=sort_rules_alpha)
                if(udt_count):
                    iudts.sort(key=sort_udts_alpha)
            for i in irules:
                display += '%03d: %s\n' % (
                    self.rules[i]['index'], self.rules[i]['name'])
            if(udt_count):
                display += '\nUDTS\n'
                for i in iudts:
                    display += '%03d: %s\n' % (
                        self.udts[i]['index'], self.udts[i]['name'])
        return display
