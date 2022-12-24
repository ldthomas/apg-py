''' @file apg_py/lib/parser.py @brief The APG parser.'''

# from pprint import pprint
from apg_py.lib import identifiers as id
from apg_py.lib.backreferences import BackrefenceStack


class ParserResult:
    '''A convenience class for the parser's results.'''

    def __init__(cls, parser):
        '''Initialize the this result object from the parser object.'''
        # For the parser to be successful, the state must be
        # MATCH or EMPTY and the parser must match the full (sub)input string.
        cls.success = (parser.state != id.NOMATCH
                       and parser.phrase_index == parser.sub_end)
        # the state identifier
        cls.state = parser.state
        # the state as human readable text
        cls.STATE = id.dict.get(parser.state)
        # the number of input characters (phrase integers) matched
        cls.phrase_length = parser.phrase_index - parser.sub_begin
        # the total number of input characters
        cls.input_length = len(parser.input)
        # the beginning character index of the substring to parse
        cls.sub_begin = parser.sub_begin
        # the ending character index of the substring to parse
        cls.sub_end = parser.sub_end
        # the total length (number of character) in the substring to parse
        cls.sub_length = parser.sub_end - parser.sub_begin
        # the number of parse tree nodes processed
        cls.node_hits = parser.node_hits
        # the maximum parse tree depth reached
        cls.max_tree_depth = parser.max_tree_depth
        # the maximum phrase length reached by the parser -
        # likely to be exactly or close to the point of failure
        # if the state is NOMATCH
        cls.max_phrase_length = parser.max_phrase_length

    def __str__(cls):
        '''Generate a string representation of the parser state.
        The string will be displayed by print() function.
        @returns Returns the string representation to display.
        '''
        display = '%19s: %s\n' % ('success', str(cls.success))
        display += '%19s: %s\n' % ('state', str(cls.state))
        display += '%19s: %s\n' % ('STATE', str(cls.STATE))
        display += '%19s: %s\n' % ('input_length', str(cls.input_length))
        display += '%19s: %s\n' % ('sub_begin', str(cls.sub_begin))
        display += '%19s: %s\n' % ('sub_end', str(cls.sub_end))
        display += '%19s: %s\n' % ('sub_length', str(cls.sub_length))
        display += '%19s: %s\n' % ('phrase_length', str(cls.phrase_length))
        display += '%19s: %s\n' % ('max_phrase_length',
                                   str(cls.max_phrase_length))
        display += '%19s: %s\n' % ('node_hits', str(cls.node_hits))
        display += '%19s: %s\n' % ('max_tree_depth', str(cls.max_tree_depth))
        return display


class Parser:
    '''The Parser class for parsing an APG grammar.'''

    def __init__(self, grammar):
        '''The Parser class constructor.
        @param grammar The grammar object generated from an SABNF grammar
        by the API (see @ref api.py).'''

        self.rules = grammar.rules
        self.udts = grammar.udts
        self.rule_count = len(self.rules)
        self.udt_count = len(self.udts)
        self.trace = None
        self.ast = None
        self.stats = None
        self.tree_depth_limit = id.MAX_INT
        self.node_hits_limit = id.MAX_INT
        self.max_tree_depth = 0
        self.tree_depth = 0
        self.node_hits = 0
        self.max_phrase_length = 0
        self.opSelect = {
            id.ALT: self.opALT,
            id.CAT: self.opCAT,
            id.REP: self.opREP,
            id.RNM: self.opRNM,
            id.TLS: self.opTLS,
            id.TBS: self.opTBS,
            id.TRG: self.opTRG,
            id.UDT: self.opUDT,
            id.AND: self.opAND,
            id.NOT: self.opNOT,
            id.BKR: self.opBKR,
            id.BKA: self.opBKA,
            id.BKN: self.opBKN,
            id.ABG: self.opABG,
            id.AEN: self.opAEN,
        }
        self.opSelectBehind = {
            id.ALT: self.opALTbehind,
            id.CAT: self.opCATbehind,
            id.REP: self.opREP,
            id.RNM: self.opRNM,
            id.TLS: self.opTLSbehind,
            id.TBS: self.opTBSbehind,
            id.TRG: self.opTRGbehind,
            id.UDT: self.opUDTbehind,
            id.AND: self.opAND,
            id.NOT: self.opNOT,
            id.BKR: self.opBKRbehind,
            id.BKA: self.opBKA,
            id.BKN: self.opBKN,
            id.ABG: self.opABG,
            id.AEN: self.opAEN,
        }
        # initialize rule callback functions
        self.rule_callbacks = [None] * self.rule_count
        if(self.udt_count):
            self.udt_callbacks = [None] * self.udt_count
        else:
            self.udt_callbacks = []
        # rule indexes for quick look up
        # list of rule + UDT names for back referencing
        bkru_names = []
        bkrr_names = []
        self.rule_indexes = {}
        for rule in self.rules:
            self.rule_indexes[rule['lower']] = rule['index']
            if(rule['is_bkru']):
                bkru_names.append(rule['lower'])
            if(rule['is_bkrr']):
                bkrr_names.append(rule['lower'])
        self.udt_indexes = {}
        if(self.udt_count):
            for udt in self.udts:
                self.udt_indexes[udt['lower']] = udt['index']
            if(udt['is_bkru']):
                bkru_names.append(udt['lower'])
            if(udt['is_bkrr']):
                bkrr_names.append(udt['lower'])
        # set up for back referencing
        self.bkru_stack = None
        self.bkrr_stack = None
        if(grammar.has_bkru):
            self.bkru_stack = BackrefenceStack(bkru_names)
        if(grammar.has_bkrr):
            self.bkrr_stack = BackrefenceStack(bkrr_names)

    def add_callbacks(self, callbacks):
        '''Add callback functions to the rule name (RNM) nodes.
        Multiple calls to this function can be used to add multiple callbacks.
        @param callbacks A dictionary of named callback functions of the form
        {'rule1': func, 'rule2': func2, 'udt1': func3}. The functions should
        have the prototype
        <pre>func(callback_data)</pre>
        where callback_data is a dictionary of the form
            - 'state': ACTIVE, MATCH, EMPTY or NOMATCH
            (see @ref identifiers.py).
            Note: UDT callback function must set state to MATCH, EMPTY
            or NOMATCH on return. If UDT name begins with "u_" an EMPTY
            return will raise an Exception.
            - 'sub_begin': The index of the first character of the sub-string
            of the input string that is being parsed.
            - 'sub_end': The index of the last character of the sub-string
            of the input string that is being parsed.
            - 'phrase_index': The offset to the first character
            of the matched phrase.
            - 'phrase_length: The number of characters in the matched phrase.
            Note: UDT callback functions must set phrase_length on return.
            - 'max_phrase_length': The maximum number of matched characters.
            (Used mainly in the syntax (@ref syntax_callbacks.py) phase
            for error reporting.)
            - 'user_data': The data object passed to the parser by the user
            in @ref parser().
        '''
        items = callbacks.items()
        for item in items:
            name = item[0].lower()
            index = self.rule_indexes.get(name, None)
            if(index is None):
                # not a rule name, try UDTs
                if(self.udt_count):
                    index = self.udt_indexes.get(name, None)
                    if(index is None):
                        raise Exception(
                            'callback name is not a rule name or UDT name',
                            item[0])
                    else:
                        # it's a UDT name
                        self.udt_callbacks[index] = item[1]
                else:
                    raise Exception(
                        'callback name is not a rule name or UDT name',
                        item[0])
            else:
                # it's a rule name
                self.rule_callbacks[index] = item[1]

    def set_tree_depth_limit(self, maxt):
        '''Set a maximum tree depth.
        The parser will raise an Exception if the parse
        tree depth exceeds the specified maximum.
        @param maxt the maximum allowed parse tree depth'''

        self.tree_depth_limit = max(0, maxt)

    def set_node_hit_limit(self, maxt):
        '''Set a maximum number of node hits.
        The parser will raise an Exception if the number
        of node hits exceeds the specified maximum.
        @param maxt the maximum allowed number of node hits'''
        self.node_hits_limit = max(0, maxt)

    def parse(
            self,
            input,
            start_rule=None,
            sub_begin=0,
            sub_length=0,
            user_data=None):
        '''Parses an input string.
        @param input A tuple of positive integers representing
        the input string.
        @param start_rule Name of the grammar's start rule
            (defaults to first rule of the SABNF grammar.)
        @param sub_begin The index of the first integer of the substring
            of the input to parse.
        @param sub_length The length of the substring to parse
            (<=0 indicates end of input string.)
        @param user_data Data which will be passed to the callback functions
            strictly for user's use.
            '''

        # initialize
        if(start_rule):
            # search for rule name
            lower = start_rule.lower()
            self.start_rule = None
            for rule in self.rules:
                if(rule['lower'] == lower):
                    self.start_rule = rule['index']
                    break
            if(self.start_rule is None):
                raise Exception('start rule not a valid rule name', start_rule)
        else:
            # use the first rule
            self.start_rule = 0
        self.input = input
        self.sub_begin = sub_begin
        input_len = len(input)
        if(sub_length > 0):
            self.sub_end = self.sub_begin + sub_length
            if(self.sub_end > input_len):
                self.sub_end = input_len
        else:
            self.sub_end = input_len
        # verify that all UDT callbacks are set, if any
        if(self.udt_count):
            for udt in self.udts:
                index = udt['index']
                name = udt['name']
                cb = self.udt_callbacks[index]
                if(cb is None):
                    raise Exception(
                        'All UDTs require a callback function. None for '
                        + name)
        if(self.ast):
            # initialize the AST
            self.ast.input = input
            self.ast.indexStack.clear()
            self.ast.records.clear()
        self.max_phrase_length = 0
        self.node_hits = 0
        self.tree_depth = 0
        self.max_tree_depth = 0
        self.state = id.ACTIVE
        self.phrase_index = self.sub_begin
        self.lookaround = 0
        self.current_look_direction = id.LOOKAROUND_NONE
        # dummy opcode for start rule
        self.opcodes = ({'type': id.RNM, 'index': self.start_rule},)
        self.cbData = {'state': id.ACTIVE,
                       'input': self.input,
                       'sub_begin': self.sub_begin,
                       'sub_end': self.sub_end,
                       'phrase_index': self.sub_begin,
                       'phrase_length': 0,
                       'max_phrase_length': 0,
                       'user_data': user_data}
        self.opExecute(0)
        return ParserResult(self)

    def opALT(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        state = id.NOMATCH
        for childOp in op['children']:
            self.state = id.ACTIVE
            if(self.bkru_stack):
                saveu = self.bkru_stack.save_state()
            if(self.bkrr_stack):
                saver = self.bkrr_stack.save_state()
            self.opExecute(childOp)
            if(self.state == id.NOMATCH):
                # reset phrase index on failure
                self.phrase_index = index
                if(self.bkru_stack):
                    self.bkru_stack.restore_state(saveu)
                if(self.bkrr_stack):
                    self.bkrr_stack.restore_state(saver)
            else:
                # ALT succeeds when first child succeeds
                state = id.MATCH if(self.phrase_index > index) else id.EMPTY
                break
        self.state = state

    def opALTbehind(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        state = id.NOMATCH
        for childOp in reversed(op['children']):
            self.state = id.ACTIVE
            self.opExecute(childOp)
            if(self.state == id.NOMATCH):
                # reset phrase index on failure
                self.phrase_index = index
            else:
                # ALT succeeds when first child succeeds
                state = id.MATCH
                break
        self.state = state

    def opCAT(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        if(self.ast and self.lookaround == 0):
            savedAstState = self.ast.save_state()
        index = self.phrase_index
        state = id.MATCH
        if(self.bkru_stack):
            saveu = self.bkru_stack.save_state()
        if(self.bkrr_stack):
            saver = self.bkrr_stack.save_state()
        for childOp in op['children']:
            self.state = id.ACTIVE
            self.opExecute(childOp)
            if(self.state == id.NOMATCH):
                # CAT fails if any child fails
                self.phrase_index = index
                state = id.NOMATCH
                if(self.bkru_stack):
                    self.bkru_stack.restore_state(saveu)
                if(self.bkrr_stack):
                    self.bkrr_stack.restore_state(saver)
                if(self.ast and self.lookaround == 0):
                    self.ast.restore_state(savedAstState)
                break
        self.state = state

    def opCATbehind(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        if(self.ast and self.lookaround == 0):
            savedAstState = self.ast.save_state()
        index = self.phrase_index
        state = id.MATCH
        for childOp in reversed(op['children']):
            self.state = id.ACTIVE
            self.opExecute(childOp)
            if(self.state == id.NOMATCH):
                # CAT fails if any child fails
                self.phrase_index = index
                state = id.NOMATCH
                if(self.ast and self.lookaround == 0):
                    self.ast.restore_state(savedAstState)
                break
        self.state = state

    def opREP(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        repCount = 0
        index = self.phrase_index
        while(True):
            if(self.phrase_index >= self.sub_end):
                # exit on end of string
                break
            # execute the child node
            self.state = id.ACTIVE
            if(self.bkru_stack):
                saveu = self.bkru_stack.save_state()
            if(self.bkrr_stack):
                saver = self.bkrr_stack.save_state()
            if(self.ast and self.lookaround == 0):
                savedAstState = self.ast.save_state()
            self.opExecute(op_index + 1)
            if(self.state == id.MATCH):
                i = 0
            if(self.state == id.EMPTY):
                # end if child node return EMPTY (prevents infinite loop)
                break
            if(self.state == id.NOMATCH):
                # end if the child node fails
                if(self.bkru_stack):
                    self.bkru_stack.restore_state(saveu)
                if(self.bkrr_stack):
                    self.bkrr_stack.restore_state(saver)
                if(self.ast and self.lookaround == 0):
                    self.ast.restore_state(savedAstState)
                break
            repCount += 1
            if(repCount == op['max']):
                # end when the repetition count has maxed out
                break
        # done with repetitions, evaluate the match count
        # abs() keeps the phrase length positive in look behind mode
        #       - in this case the phrase index is moving backwards
        repPhraseLength = abs(self.phrase_index - index)
        if(self.state == id.EMPTY):
            # REP always succeeds when child node returns EMPTY
            # this may not seem obvious, but that's the way it works out
            self.state = id.EMPTY if(
                repPhraseLength == 0) else id.MATCH
        elif(repCount >= op['min']):
            self.state = id.EMPTY if(
                repPhraseLength == 0) else id.MATCH
        else:
            self.state = id.NOMATCH

    def opRNM(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        parentOps = self.opcodes
        op = self.opcodes[op_index]
        rule = self.rules[op['index']]
        lower = rule['lower']
        self.opcodes = rule['opcodes']
        if(rule['has_bkrr']):
            saver = self.bkrr_stack.save_state()
        self.state = id.ACTIVE
        phrase_index = self.phrase_index
        phrase_length = 0
        if(self.rule_callbacks[op['index']]):
            # handle rule callback function (down)
            self.cbData['state'] = id.ACTIVE
            self.cbData['phrase_index'] = phrase_index
            self.cbData['phrase_length'] = 0
            self.cbData['max_phrase_length'] = self.max_phrase_length
            self.rule_callbacks[op['index']](self.cbData)
        if(self.ast and self.lookaround == 0):
            savedAstState = self.ast.save_state()
            self.ast.down(lower)
        self.opExecute(0)
        if(self.current_look_direction == id.LOOKAROUND_BEHIND):
            # phrase index is moving backwards here
            phrase_length = phrase_index - self.phrase_index
            phrase_index = self.phrase_index
        else:
            phrase_length = self.phrase_index - phrase_index
        if(self.rule_callbacks[op['index']]):
            # handle rule callback function (up)
            self.cbData['state'] = self.state
            self.cbData['phrase_length'] = phrase_length
            if(self.current_look_direction == id.LOOKAROUND_BEHIND):
                self.cbData['phrase_index'] = self.phrase_index
            else:
                self.cbData['phrase_index'] = phrase_index
            self.rule_callbacks[op['index']](self.cbData)
        # handle back referencing, if any
        if(self.state == id.NOMATCH):
            if(self.ast and self.lookaround == 0):
                self.ast.restore_state(savedAstState)
        else:
            if(self.ast and self.lookaround == 0):
                self.ast.up(lower, phrase_index, phrase_length)
            # save the phrase for later back referencing
            if(rule['is_bkru']):
                self.bkru_stack.save_phrase(
                    lower, phrase_index, phrase_length)
            if(rule['is_bkrr']):
                self.bkrr_stack.save_phrase(
                    lower, phrase_index, phrase_length)
        if(rule['has_bkrr']):
            # pop the recursive back referencing stack
            # Note: there is a conflict here if a rule is both
            # recursive and recursively back referenced.
            # The recursive back reference will always fail because
            # it is both saved and removed on restore.
            self.bkrr_stack.restore_state(saver)
        self.opcodes = parentOps

    def opTLS(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        length = len(op['string'])
        if(length == 0):
            # EMPTY match allowed, only in TLS
            self.state = id.EMPTY
            return
        state = id.NOMATCH
        if(index + length <= self.sub_end):
            state = id.MATCH
            for char in op['string']:
                ichar = self.input[index]
                if(ichar >= 65 and ichar <= 90):
                    ichar += 32
                if(char != ichar):
                    state = id.NOMATCH
                    break
                index += 1
        self.state = state
        if(state == id.MATCH):
            self.phrase_index += length

    def opTLSbehind(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        length = len(op['string'])
        if(length == 0):
            # EMPTY match allowed, only in TLS
            self.state = id.EMPTY
            return
        state = id.NOMATCH
        if(index - length >= 0):
            state = id.MATCH
            index -= length
            for char in op['string']:
                ichar = self.input[index]
                if(ichar >= 65 and ichar <= 90):
                    ichar += 32
                if(char != ichar):
                    state = id.NOMATCH
                    break
                index += 1
        self.state = state
        if(state == id.MATCH):
            self.phrase_index -= length

    def opTBS(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        length = len(op['string'])
        state = id.NOMATCH
        if(index + length <= self.sub_end):
            state = id.MATCH
            for char in op['string']:
                if(char != self.input[index]):
                    state = id.NOMATCH
                    break
                index += 1
        self.state = state
        if(state == id.MATCH):
            self.phrase_index += length

    def opTBSbehind(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        length = len(op['string'])
        state = id.NOMATCH
        if(index - length >= 0):
            state = id.MATCH
            index -= length
            for char in op['string']:
                if(char != self.input[index]):
                    state = id.NOMATCH
                    break
                index += 1
        self.state = state
        if(state == id.MATCH):
            self.phrase_index -= length

    def opTRG(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index
        state = id.NOMATCH
        if(index < self.sub_end):
            char = self.input[index]
            if(char >= op['min'] and char <= op['max']):
                state = id.MATCH
                self.phrase_index += 1
        self.state = state

    def opTRGbehind(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        index = self.phrase_index - 1 if(self.phrase_index > 0) else 0
        state = id.NOMATCH
        if(index > 0):
            char = self.input[index]
            if(char >= op['min'] and char <= op['max']):
                state = id.MATCH
                self.phrase_index -= 1
        self.state = state

    def UDTValidate(
            self,
            state,
            phrase_index,
            phrase_length,
            last_index,
            name,
            empty):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        def raiseEx(msg):
            raise Exception('UDT ' + name + ' ' + msg)
        if(state == id.MATCH):
            if(phrase_length <= 0):
                raiseEx(
                    'matched phrase length must be > 0: ' +
                    str(phrase_length))
            if(phrase_index + phrase_length > last_index):
                raiseEx('phrase_length cannot extend past end of substring')
            return
        if(state == id.EMPTY):
            if(empty is not True):
                raiseEx('not allowed to return EMPTY state')
            if(phrase_length):
                raiseEx(
                    'EMPTY state must have 0 phrase length: ' +
                    str(phrase_length))
            return
        if(state == id.NOMATCH):
            return
        if(state == id.ACTIVE):
            raiseEx('must return EMPTY, MATCH or NOMATCH')
        raiseEx('returned unrecognized state: ' + str(state))

    def opUDT(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        udt = self.udts[op['index']]
        lower = udt['lower']
        self.cbData['state'] = id.ACTIVE
        self.cbData['phrase_index'] = self.phrase_index
        self.cbData['phrase_length'] = 0
        self.cbData['max_phrase_length'] = self.max_phrase_length
        self.udt_callbacks[op['index']](self.cbData)
        self.UDTValidate(
            self.cbData['state'],
            self.phrase_index,
            self.cbData['phrase_length'],
            self.sub_end,
            udt['name'],
            udt['empty'])
        self.state = self.cbData['state']
        # handle back referencing, if any
        if(self.state != id.NOMATCH):
            if(self.ast and self.lookaround == 0):
                self.ast.down(lower)
                self.ast.up(
                    lower,
                    self.cbData['phrase_index'],
                    self.cbData['phrase_length'])
            # save the phrase for later back referencing
            if(udt['is_bkru']):
                self.bkru_stack.save_phrase(
                    udt['lower'],
                    self.cbData['phrase_index'],
                    self.cbData['phrase_length'])
            if(udt['is_bkrr']):
                self.bkrr_stack.save_phrase(
                    udt['lower'],
                    self.cbData['phrase_index'],
                    self.cbData['phrase_length'])
        self.phrase_index += self.cbData['phrase_length']

    def opUDTbehind(self, op_index):
        '''UDT operator not allowed in look behind mode.'''
        op = self.opcodes[op_index]
        udt = self.udts[op['index']]
        msg = 'UDT('
        msg += udt['name']
        msg += ') called. '
        msg += 'UDTs not allowed in look behind mode (operators && and !!).'
        raise Exception(msg)

    def opAND(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        index = self.phrase_index
        self.state = id.ACTIVE
        self.lookaround += 1
        saveDir = self.current_look_direction
        self.current_look_direction = id.LOOKAROUND_AHEAD
        if(self.bkrr_stack):
            saver = self.bkrr_stack.save_state()
        if(self.bkru_stack):
            saveu = self.bkru_stack.save_state()
        #
        self.opExecute(op_index + 1)
        #
        if(self.bkrr_stack):
            self.bkrr_stack.restore_state(saver)
        if(self.bkru_stack):
            self.bkru_stack.restore_state(saveu)
        if(self.state == id.EMPTY
           or self.state == id.MATCH):
            # AND succeeds if child succeeds
            self.state = id.EMPTY
        else:
            # AND fails if child fails
            self.state = id.NOMATCH
        self.phrase_index = index
        self.lookaround -= 1
        self.current_look_direction = saveDir

    def opNOT(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        index = self.phrase_index
        self.state = id.ACTIVE
        self.lookaround += 1
        saveDir = self.current_look_direction
        self.current_look_direction = id.LOOKAROUND_AHEAD
        if(self.bkrr_stack):
            saver = self.bkrr_stack.save_state()
        if(self.bkru_stack):
            saveu = self.bkru_stack.save_state()
        #
        self.opExecute(op_index + 1)
        #
        if(self.bkrr_stack):
            self.bkrr_stack.restore_state(saver)
        if(self.bkru_stack):
            self.bkru_stack.restore_state(saveu)
        if(self.state == id.NOMATCH):
            # NOT succeeds if child fails
            self.state = id.EMPTY
        else:
            # NOT fails if child succeeds
            self.state = id.NOMATCH
        self.phrase_index = index
        self.lookaround -= 1
        self.current_look_direction = saveDir

    def opBKA(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        index = self.phrase_index
        self.state = id.ACTIVE
        self.lookaround += 1
        saveDir = self.current_look_direction
        self.current_look_direction = id.LOOKAROUND_BEHIND
        if(self.bkrr_stack):
            saver = self.bkrr_stack.save_state()
        if(self.bkru_stack):
            saveu = self.bkru_stack.save_state()
        #
        self.opExecute(op_index + 1)
        #
        if(self.bkrr_stack):
            self.bkrr_stack.restore_state(saver)
        if(self.bkru_stack):
            self.bkru_stack.restore_state(saveu)
        if(self.state == id.EMPTY
           or self.state == id.MATCH):
            # BKA succeeds if child succeeds
            self.state = id.EMPTY
        else:
            # BKA fails if child fails
            self.state = id.NOMATCH
        self.phrase_index = index
        self.lookaround -= 1
        self.current_look_direction = saveDir

    def opBKN(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        index = self.phrase_index
        self.state = id.ACTIVE
        self.lookaround += 1
        saveDir = self.current_look_direction
        self.current_look_direction = id.LOOKAROUND_BEHIND
        if(self.bkrr_stack):
            saver = self.bkrr_stack.save_state()
        if(self.bkru_stack):
            saveu = self.bkru_stack.save_state()
        #
        self.opExecute(op_index + 1)
        #
        if(self.bkrr_stack):
            self.bkrr_stack.restore_state(saver)
        if(self.bkru_stack):
            self.bkru_stack.restore_state(saveu)
        if(self.state == id.NOMATCH):
            # NOT succeeds if child fails
            self.state = id.EMPTY
        else:
            # NOT fails if child succeeds
            self.state = id.NOMATCH
        self.phrase_index = index
        self.lookaround -= 1
        self.current_look_direction = saveDir

    def opBKR(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        if(op['bkr_mode'] == id.BKR_MODE_UM):
            phrase = self.bkru_stack.get_phrase(op['lower'])
        elif(op['bkr_mode'] == id.BKR_MODE_RM):
            phrase = self.bkrr_stack.get_phrase(op['lower'])
        else:
            raise Exception('BKR mode not recognized')
        bkrIndex = phrase[0]
        bkrLength = phrase[1]
        if(bkrLength == 0):
            self.state = id.EMPTY
            return
        state = id.NOMATCH
        if(self.phrase_index + bkrLength <= self.sub_end):
            state = id.MATCH
            if(op['bkr_case'] == id.BKR_MODE_CS):
                for i in range(bkrLength):
                    bkrChar = self.input[bkrIndex + i]
                    inputChar = self.input[self.phrase_index + i]
                    if(bkrChar != inputChar):
                        state = id.NOMATCH
                        break
            elif(op['bkr_case'] == id.BKR_MODE_CI):
                for i in range(bkrLength):
                    bkrChar = self.input[bkrIndex + i]
                    inputChar = self.input[self.phrase_index + i]
                    if(bkrChar >= 65 and bkrChar <= 90):
                        bkrChar += 32
                    if(inputChar >= 65 and inputChar <= 90):
                        inputChar += 32
                    if(bkrChar != inputChar):
                        state = id.NOMATCH
                        break
            else:
                raise Exception('BKR case not recognized')

        self.state = state
        if(state == id.MATCH):
            self.phrase_index += bkrLength
        return

    def opBKRbehind(self, op_index):
        '''Back references not allowed in look behind mode.'''
        op = self.opcodes[op_index]
        msg = 'BKR('
        msg += op['name']
        msg += ') called. '
        msg += 'Back referencing not allowed in look behind mode '
        msg += '(operators && and !!).'
        raise Exception(msg)

    def opABG(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        if(self.phrase_index == 0):
            # ABG, beginning of string anchor succeeds
            # if index is first character of the input string
            # (not first character of substring, if any)
            self.state = id.EMPTY
        else:
            self.state = id.NOMATCH

    def opAEN(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        if(self.phrase_index == len(self.input)):
            # AEN, end of string anchor succeeds
            # if index is the last character
            # (not last character of substring, if any)
            self.state = id.EMPTY
        else:
            self.state = id.NOMATCH

    def opExecute(self, op_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        op = self.opcodes[op_index]
        opSelect = self.opSelectBehind if(
            self.current_look_direction
            == id.LOOKAROUND_BEHIND) else self.opSelect
        opFunc = opSelect.get(op['type'], None)
        index = self.phrase_index
        self.execDown(op)
        opFunc(op_index)
        self.execUp(op, index)

    def execDown(self, op):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        if(self.trace):
            self.trace.down(op)
        self.tree_depth += 1
        self.node_hits += 1
        if(self.tree_depth >= self.tree_depth_limit):
            raise Exception(
                'parse tree depth limit exceeded, limit = %d' %
                self.tree_depth_limit)
        if(self.node_hits >= self.node_hits_limit):
            raise Exception(
                'node hits limit exceeded, limit = %d' %
                self.node_hits_limit)
        if(self.tree_depth > self.max_tree_depth):
            self.max_tree_depth = self.tree_depth

    def execUp(self, op, begin_index):
        '''Only called internally by the parser,
        never called explicitly by the user.
        '''
        self.tree_depth -= 1
        if(self.lookaround == 0):
            totalLength = self.phrase_index - self.sub_begin
            if(totalLength > self.max_phrase_length):
                self.max_phrase_length = totalLength
        if(self.trace):
            self.trace.up(op, begin_index)
        if(self.stats):
            self.stats.collect(op)
