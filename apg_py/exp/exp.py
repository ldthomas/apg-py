''' @file apg_py/exp/exp.py
@brief ApgExp - a RegExp-like pattern matching engine.
'''
import sys
import types
import copy
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.ast import Ast
from apg_py.lib.trace import Trace
from apg_py.api.api import Api


class Result():
    '''A class for returning the results of a pattern match.
    '''

    def __init__(
            self,
            source,
            begin,
            length,
            node_hits,
            tree_depth,
            rules,
            names,
            ast,
            codes=False):
        '''The Result class constructor. Only called internally by ApgExp'''
        ending = begin + length
        self.source = source
        self.index = begin
        self.indices = [begin, ending]
        self.match = source[begin:ending]
        self.left_context = source[:begin]
        self.right_context = source[ending:]
        self.codes = codes
        self.rules = rules
        self.names = names
        self.ast = ast.copy() if(ast) else None
        self.node_hits = node_hits
        self.max_tree_depth = tree_depth

    def __str__(self):
        '''print(Result) will call this function for a display of the object.
        @returns Returns the display string.'''
        string = '         match: ' + str(self.match)
        string += '\n         index: ' + str(self.index)
        string += '\n       indices: ' + str(self.indices)
        string += '\n  left_context: ' + str(self.left_context)
        string += '\n right_context: ' + str(self.right_context)
        string += '\n     node hits: ' + str(self.node_hits)
        string += '\nmax tree depth: ' + str(self.max_tree_depth)
        if(len(self.rules)):
            string += '\n\nrules: ' + str(len(self.rules))
        for key, value in self.rules.items():
            if(len(value) == 0):
                string += '\n' + self.names[key]
                string += '[0]: <undefined>'
            for i in range(len(value)):
                # print('key: ' + key, end=' ')
                # print('value[' + str(i) + ']: ', end='')
                # print(value[i])
                string += '\n' + self.names[key]
                string += '[' + str(i) + ']: '
                if(self.codes):
                    string += '('
                    for val in value[i]:
                        string += str(val) + ','
                    string += ')'
                    i = 0
                else:
                    string += utils.tuple_to_string(value[i])
                    # string += '\n'
        return string


class ApgExp():
    '''The ApgExp class provides a pattern-matching engine similar
    to JavaScript's [RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp)'''

    def __init__(self, pattern, flags=''):
        '''The ApgExp constructor.
        @param pattern The SABNF pattern to match.
        @param flags A string of characters specifying
        the operation characteristics. May be any of the following:
            - c display results as lists of integer "character" codes
            - g global matching mode - last_index follows
        the previous matched phrase
            - t trace a trace of each match attempt is displayed
            - y sticky similar to global except that the next match
        must be at exactly last_index

        Note that:
            - letters may be in any order
            - multiple occurrances of letters allowed, the last occurrance wins
            - the global, g, and sticky, y, flags are mutually exclusive
            - any letter not in this list will raise and exception
        '''
        self._character_codes_ = False
        self._global_ = False
        self._trace_ = False
        self._sticky_ = False
        for ll in flags:
            if(ll == 'c'):
                self._character_codes_ = True
            elif(ll == 'g'):
                self._global_ = True
                self._sticky_ = False
            elif(ll == 't'):
                self._trace_ = True
            elif(ll == 'y'):
                self._sticky_ = True
                self._global_ = False
            else:
                raise Exception('flag ' + ll + ' not recognized')
        self.flags = ''
        if(self._character_codes_):
            self.flags += 'c'
        if(self._global_):
            self.flags += 'g'
        if(self._trace_):
            self.flags += 't'
        if(self._sticky_):
            self.flags += 'y'

        api = Api()
        api.generate(pattern)
        if(api.errors):
            raise Exception('Pattern syntax error: \n' + api.display_errors())
        self.pattern = pattern
        self.grammar = api.grammar
        self.parser = Parser(self.grammar)
        self.__ast = None
        if(self._trace_):
            mode = 'd' if(self._character_codes_) else 'dc'
            Trace(self.parser, mode=mode)
        self.rules = {}
        self.names = {}
        self.last_index = 0
        self.max_tree_depth = 0
        self.max_node_hits = 0

    def __callback_factory(self, name):
        def fn(state, source, index, length, data):
            if(state == id.SEM_POST):
                self.rules[name.lower()].append(source[index:index + length])
        return fn

    def __get_input(self, input):
        if(self._character_codes_):
            if(isinstance(input, tuple)):
                input_tuple = input
            else:
                # input must be a list or tuple of integers
                msg = '"c" flag is set - '
                msg += 'input must be a tuple of integers'
                raise Exception(msg)
        else:
            if(isinstance(input, str)):
                input_tuple = utils.string_to_tuple(input)
            else:
                # input must be a string
                msg = '"c" flag is not set - '
                msg += 'input must be a string'
                raise Exception(msg)
        return input_tuple

    def set_tree_depth(self, depth):
        '''Limit the maximum tree depth that the parser may make.
        @param depth The maximum allowed tree node depth.
        If the parser exceeds this limit an exception is raised.'''
        self.max_tree_depth = max(0, depth)
        self.parser.set_node_hit_limit(self.max_tree_depth)

    def set_node_hits(self, hits):
        '''Limit the maximum number of parse tree nodes that the parser may visit.
        @param hits The maximum allowed number of node hits the parser can make.
        If the parser exceeds this limit an exception is raised.'''
        self.max_node_hits = max(0, hits)
        self.parser.set_node_hit_limit(self.max_node_hits)

    def define_udts(self, callbacks):
        '''UDTs are user-written callback functions for specialized pattern matching.
        Callback functions must be defined for all UDTs in the SABNF grammar syntax.
        @param callbacks A dictionary defining one or more callbacks.
        Multiple calls may be made until all UDT callback are defined.
        callbacks = {'udt1': func[[, 'udt2': func2], etc.]}
        '''
        if(len(self.parser.udts)):
            items = callbacks.items()
            for item in items:
                name = item[0].lower()
                name_found = False
                for udt in self.parser.udts:
                    if(udt['lower'] == name):
                        name_found = True
                        break
                if(not name_found):
                    raise(Exception('UDT name ' + name + ' not found'))
            # if we get here, all names ok
            self.parser.add_callbacks(callbacks)
        else:
            raise Exception('pattern has no UDTs')

    def include(self, names=[]):
        '''Define the list of rule/UDT name phrases to be included
        in the matched results.
        @param names A list of rule/UDT names.
        An empty list will include ALL rules and UDTs.
        Invalid names will
        raise an Exception.
        '''
        self.__ast = Ast(self.parser)
        if(len(names) == 0):
            # add all names
            for rule in self.parser.rules:
                self.names[rule['lower']] = rule['name']
                self.rules[rule['lower']] = []
                self.__ast.add_callback(
                    rule['name'], self.__callback_factory(
                        rule['name']))
            for udt in self.parser.udts:
                self.names[udt['lower']] = udt['name']
                self.rules[udt['lower']] = []
                self.__ast.add_callback(
                    udt['name'], self.__callback_factory(
                        udt['name']))
        else:
            # add only names in list
            for name in names:
                # find the name
                name_found = False
                name_lower = name.lower()
                for rule in self.parser.rules:
                    if(rule['lower'] == name_lower):
                        self.names[rule['lower']] = rule['name']
                        self.rules[rule['lower']] = []
                        self.__ast.add_callback(
                            rule['name'], self.__callback_factory(
                                rule['name']))
                        name_found = True
                        break
                if(not name_found and len(self.parser.udts)):
                    for udt in self.parser.udts:
                        if(udt['lower'] == name_lower):
                            self.names[udt['lower']] = udt['name']
                            self.rules[udt['lower']] = []
                            self.__ast.add_callback(
                                udt['name'], self.__callback_factory(
                                    udt['name']))
                            name_found = True
                            break
                if(not name_found):
                    raise Exception(name + ' not a rule or UDT name')

    def exclude(self, names=[]):
        '''Define the list of rule/UDT name phrases to be excluded
        from the matched results.
        @param names A list of rule/UDT names.
        An empty list will include ALL rules and UDTs.
        Invalid names will
        raise an Exception.
        '''
        self.__ast = Ast(self.parser)
        if(len(names) == 0):
            # include all names
            self.include(names)
            return
        # generate a list of all names
        names_lower = []
        for name in names:
            names_lower.append(name.lower())
        for rule in self.parser.rules:
            if(rule['lower'] not in names_lower):
                self.names[rule['lower']] = rule['name']
                self.rules[rule['name']] = []
                self.__ast.add_callback(
                    rule['name'], self.__callback_factory(
                        rule['name']))
        for udt in self.parser.udts:
            if(udt['lower'] not in names_lower):
                self.names[udt['lower']] = udt['name']
                self.rules[udt['name']] = []
                self.__ast.add_callback(
                    udt['name'], self.__callback_factory(
                        udt['name']))

    def exec(self, input):
        '''Execute the pattern match.
        Search for a match begins at last_index.
        (Note: last_index can be set prior to calling exec()
        with ApgExp.last_index = value.)
        If the g or y flag is set, last_index is set to the
        next character beyond the matched pattern
        or incremented by one if the matched pattern is empty.
        If the pattern is not matched, last_index is always set to 0.
        @param input The input as a string or tuple of character codes
        if the "c" flag is set.
        @returns Returns the result object if pattern is matched.
        None otherwise.
        '''
        input_tuple = self.__get_input(input)
        sub_beg = self.last_index
        sub_end = len(input_tuple)
        if(sub_beg >= sub_end):
            # user may have set bad value for last_index
            return None
        match_result = None
        if(self._sticky_):
            if(self._trace_):
                print()
                print('trace beginning at sticky character ' + str(sub_beg))
            parser_result = self.parser.parse(input_tuple, sub_begin=sub_beg)
            if(parser_result.state == id.MATCH
               or parser_result.state == id.EMPTY):
                # set up return result
                self.last_index = sub_beg + \
                    max(1, parser_result.phrase_length)
                if(len(self.rules)):
                    data = {}
                    self.__ast.translate(data)
                match_result = Result(
                    input, sub_beg,
                    parser_result.phrase_length,
                    parser_result.node_hits,
                    parser_result.max_tree_depth,
                    self.rules, self.names, self.__ast, self._character_codes_)
        else:
            while sub_beg < sub_end:
                if(self._trace_):
                    print()
                    print('trace beginning at character ' + str(sub_beg))
                parser_result = self.parser.parse(
                    input_tuple, sub_begin=sub_beg)
                self.last_index = 0
                if(parser_result.state == id.MATCH
                   or parser_result.state == id.EMPTY):
                    # set up return result
                    if(self._global_):
                        self.last_index = sub_beg + \
                            max(1, parser_result.phrase_length)
                    if(len(self.rules)):
                        for key in self.rules.keys():
                            # clear the rules
                            self.rules[key] = []
                        data = {}
                        self.__ast.translate(data)
                    match_result = Result(
                        input, sub_beg,
                        parser_result.phrase_length,
                        parser_result.node_hits,
                        parser_result.max_tree_depth,
                        self.rules, self.names, self.__ast,
                        self._character_codes_)
                    break
                sub_beg += 1
        return match_result

    def test(self, input):
        '''Same as @ref exec() except for the return.
        @returns Returns True if a pattern match is found, False otherwise.'''
        input_tuple = self.__get_input(input)
        sub_beg = self.last_index
        sub_end = len(input_tuple)
        if(sub_beg >= sub_end):
            # user may have set bad value for last_index
            return False
        test_result = False
        if(self._sticky_):
            if(self._trace_):
                print()
                print('trace beginning at sticky character ' + str(sub_beg))
            parser_result = self.parser.parse(input_tuple, sub_begin=sub_beg)
            if(parser_result.state == id.MATCH
               or parser_result.state == id.EMPTY):
                self.last_index = sub_beg +  \
                    max(1, parser_result.phrase_length)
                test_result = True
            else:
                self.last_index = 0
        else:
            while sub_beg < sub_end:
                if(self._trace_):
                    print()
                    print('trace beginning at character ' + str(sub_beg))
                parser_result = self.parser.parse(
                    input_tuple, sub_begin=sub_beg)
                self.last_index = 0
                if(parser_result.state == id.MATCH
                   or parser_result.state == id.EMPTY):
                    # set up return result
                    if(self._global_):
                        self.last_index = sub_beg + \
                            max(1, parser_result.phrase_length)
                    test_result = True
                    break
                sub_beg += 1
        return test_result

    def split(self, input, limit=0):
        '''Split the input string on the matched delimiters.
        The ApgExp pattern defines the delimiters.
        Works similar to the
        [JavaScript String.split()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split)
        function.
        All flags except the character code flag "c" are ignored.
        If the "c" flag is set, substitute "tuple of character codes" for string.
          - if the input string is empty, the output list contains
          a single empty string
          - if the pattern matches the entire string, the output list contains
          a single empty string.
          - if no pattern matches are found in the input string,
          the output list contains a single string which
          is a copy of the input string.
          - if the pattern finds multiple matches, the output list contains
          a each of the strings between the matches
          - if the pattern matches the empty string, the output will be a list
          of the single characters.
        @param input The input string or tuple of character codes.
        @param limit If limit > 0 only limit delimiters are matched.
        The trailing string suffix, if any, is ignored.
        @returns Returns a list of strings or character code tuples.
        '''
        def gen_output(intervals):
            # from a list of index intervals, generate the
            # list of output strings or tuples
            if(len(intervals) == 0):
                if(self._character_codes_):
                    return [()]
                return ['']
            gen = []
            for interval in intervals:
                tup = input_tuple[interval[0]:interval[1]]
                if(self._character_codes_):
                    gen.append(tup)
                else:
                    gen.append(utils.tuple_to_string(tup))
            return gen

        input_tuple = self.__get_input(input)
        if(len(input_tuple) == 0):
            # input is empty, return empty string or character code array
            return gen_output([])
        if(limit <= 0):
            limit = sys.maxsize
        sub_beg = 0
        sub_end = len(input_tuple)
        intervals = []
        while(sub_beg < sub_end and limit > 0):
            parser_result = self.parser.parse(
                input_tuple, sub_begin=sub_beg)
            if(parser_result.state == id.MATCH):
                limit -= 1
                intervals.append(
                    [sub_beg, sub_beg + parser_result.phrase_length])
                sub_beg += parser_result.phrase_length
            elif(parser_result.state == id.EMPTY):
                limit -= 1
                intervals.append([sub_beg, sub_beg])
                sub_beg += 1
            else:
                sub_beg += 1
        len_intervals = len(intervals)
        if(len_intervals == 0):
            # no match, return original string
            return gen_output([[0, sub_end]])
        beg = 0
        out_put = []
        for interval in intervals:
            if(beg < interval[0]):
                out_put.append([beg, interval[0]])
            beg = interval[1]
        intervals_end = intervals[len_intervals - 1][1]
        if(limit > 0):
            # add the remainder, if any
            if(intervals_end < sub_end):
                out_put.append([intervals_end, sub_end])
        return gen_output(out_put)

    def replace(self, input, replacement):
        '''Replace matched patterns. If a pattern match is found in "input"
        it will be replaced with "replacement".
        Works similar to the
        [JavaScript String.replace()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace)
        function.
        If the "g" or "y" flags are set, all matched patterns are replaced.
        Otherwise, only the first match is replaced.
        @param input The string to look for pattern matches in.
        If the "c" flag is set, input must be a tuple of integers.
        Otherwise, it is a string.
        @param replacement This may be a simple replacement string,
        a complex replacement string with special characters or
        a function that returns the replacement string.
        If the "c" flag is not set, replacement must be a string,
        possibly with special characters or
        a function that returns a string. Special string characters are:
          - $$ substitute $
          - $` substitute the matched left context
          - $& substitute the matched pattern itself
          - $' substitute the matched right context
          - ${name} substitue the matched rule/UDT name(case insensitive),
          note that if this rule has no match an empty string will be used.
        <br>
        <br>
        The function must have the prototype
          - fn(input, result) where input is the original input string
          and result is the pattern matching result object.
          The function must return a string
        <br>
        <br>
        If the "c" flag is set, replacement must be a tuple of integers
        or a function that returns a tuple of integers.
        In this case there are no special characters comparable to the string
        special characters. However, since the function gets the result
        as an argument, it can be used for the same purpose.
        The function must have the prototype:
          - fn(input, result) where input is the original input tuple
          and result is the pattern matching result object.
          The function must return a tuple of integers.
        @returns Returns the input string/tuple "input" with one or all
        matched patterns replaced with the replacement string,
        tuple or function.
        '''
        # get the result(s)
        self.last_index = 0
        res = self.exec(input)
        if(not res):
            # no pattern matches to replace
            return copy.copy(input)
        results = []
        results.append(copy.deepcopy(res))
        if(self._global_ or self._sticky_):
            while(res):
                res = self.exec(input)
                if(res):
                    results.append(copy.deepcopy(res))

        if(isinstance(replacement, types.FunctionType)):
            # handle callable function for replacement
            output = copy.copy(input)
            diff = 0
            for result in results:
                pref = output[:diff + result.indices[0]]
                suff = output[diff + result.indices[1]:]
                repl = replacement(input, result)
                if(self._character_codes_):
                    if(not isinstance(repl, tuple)):
                        msg = 'replacement function must return'
                        msg += ' a tuple of integers'
                        raise Exception(msg)
                else:
                    if(not isinstance(repl, str)):
                        msg = 'replacement function must return'
                        msg += ' a string'
                        raise Exception(msg)
                diff += len(repl) + result.indices[0] - result.indices[1]
                output = pref + repl + suff
        elif(self._character_codes_):
            if(not isinstance(replacement, tuple)):
                raise Exception(
                    'replace(): "c" flag set - input must be a tuple')
            # handle tuple replacement
            output = copy.copy(input)
            diff = 0
            for result in results:
                pref = output[:diff + result.indices[0]]
                suff = output[diff + result.indices[1]:]
                diff += len(replacement) + \
                    result.indices[0] - result.indices[1]
                output = pref + replacement + suff
        else:
            if(not isinstance(replacement, str)):
                raise Exception(
                    'replace(): "c" flag not set - input must be a string')
            # handle string replacement
            output = copy.copy(input)
            diff = 0
            for result in results:
                pref = output[:diff + result.indices[0]]
                suff = output[diff + result.indices[1]:]
                repl = replace_special_chars(replacement, result)
                diff += len(repl) + result.indices[0] - result.indices[1]
                output = pref + repl + suff
        return output


def replace_special_chars(replacement, result):
    # handle replacing special characters in replacement string
    special = copy.copy(replacement)
    special_found = True
    start = 0
    while(special_found):
        special_found = False
        for i in range(start, len(special)):
            if(special[i] == '$'):
                pref = special[:i]
                suf = special[i + 2:]
                special_found = True
                start = i + 2
                if(special[i + 1] == '$'):
                    special = pref + '$' + suf
                    break
                if(special[i + 1] == '&'):
                    special = pref + result.match + suf
                    break
                if(special[i + 1] == '`'):
                    special = pref + result.left_context + suf
                    break
                if(special[i + 1] == "'"):
                    special = pref + result.right_context + suf
                    break
                if(special[i + 1] == "{"):
                    name = None
                    for j in range(i + 2, len(special)):
                        if(special[j] == '}'):
                            name = special[i + 2:j]
                            suf = special[j + 1:]
                            # start = j + 1
                            break
                    if(not name):
                        msg = 'replace(): ${name}, name or closing bracket '
                        msg += 'not found'
                        raise Exception(msg)
                    lower = name.lower()
                    if(result.rules.get(lower)):
                        last_match = len(result.rules[lower]) - 1
                        name_string = utils.tuple_to_string(
                            result.rules[lower][last_match])
                    else:
                        # rule name did not match a string
                        name_string = ''
                    special = pref + name_string + suf
                    start = len(pref) + len(name_string)
                    break
    return special
