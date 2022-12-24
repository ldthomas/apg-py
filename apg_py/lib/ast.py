''' @file apg_py/lib/ast.py
@brief A class for creating and translating the Abstract Syntax Tree (AST).'''

import copy
from apg_py.lib import identifiers as id


def inner_add_callback(nodes, name, callback):
    '''Set a callback function for a named node.
    Records will only be kept for nodes that have a
    callback assigned to them. Called by both the original AST
    and the shallow copy of the AST passed to the pattern-matching results.
    @param nodes The list of AST nodes.
    @param name the rule or UDT name of the node
    @param callback the callback function for this node'''
    lower = name.lower()
    if(lower in nodes):
        nodes[lower] = callback
    else:
        raise Exception('add_callback name not recognized', name)


def inner_translate(input, nodes, records, data=None):
    '''Traverse the AST and call the user's callback functions for
    translation of the saved AST node phrases.
    Called by both the original AST
    and the shallow copy of the AST passed to the pattern-matching results.
    @param input The input string to the parser as a tuple of integers.
    @param nodes The list of AST nodes.
    @param records The list of AST node records.
    @param data arbitary user data to be passed to the callback functions
    '''
    i = 0
    while(i < len(records)):
        record = records[i]
        callback = nodes[record['name']]
        if(record['state'] == id.SEM_PRE):
            # Note that the callback functions could be modified or
            # removed (set to None)
            # between the parsing of the input string and the translation
            # of the AST. Therefore, there may be retained records for
            # nodes that have no callback function assigned to them.
            if(callback):
                ret = callback(
                    id.SEM_PRE,
                    input,
                    record['phrase_index'],
                    record['phrase_length'],
                    data)
                if(ret == id.SEM_SKIP):
                    callback(
                        id.SEM_POST,
                        input,
                        record['phrase_index'],
                        record['phrase_length'],
                        data)
                    i = record['that_record']
        else:
            if(callback):
                callback(
                    id.SEM_POST,
                    input,
                    record['phrase_index'],
                    record['phrase_length'],
                    data)
        i += 1


class Ast():
    '''A class for capturing the AST as the parser traverses the parse tree.'''

    def __init__(self, parser):
        '''Class constructor.
        @param parser the parser object to attach this AST object to'''
        self.parser = parser
        parser.ast = self
        self.input = []  # will be set by the parser
        self.indexStack = []
        self.records = []
        self.nodes = {}
        for rule in parser.rules:
            self.nodes[rule['lower']] = None
        for udt in parser.udts:
            self.nodes[udt['lower']] = None

    def copy(self):
        '''Make a copy suitable for adding callback functions
        and doing translations.
        This copy will not interact with the parser.
        The primary purpose of this is so the class ApgExp (@ref exp.py)
         can internally
        do an AST translation of the parsed results and also return
        a copy of the AST for the user to do a separate, independent
        translation of the pattern-matched results.
        '''
        class ast_copy():
            def __init__(cls, ast_to_copy):
                cls.input = copy.copy(ast_to_copy.input)
                cls.records = copy.deepcopy(ast_to_copy.records)
                cls.nodes = copy.copy(ast_to_copy.nodes)

            def add_callback(cls, name, callback):
                inner_add_callback(cls.nodes, name, callback)

            def translate(cls, data=None):
                inner_translate(cls.input, cls.nodes, cls.records, data)
        return ast_copy(self)

    def add_callback(self, name, callback):
        '''Add a callback function to the named AST node.
        @param name The name of the node to add the callback to.
        @param callback The callback function to add to the node.
        The function should have the prototype:<br>
        fn(state, input, index, length, data)
            - state - SEM_PRE for down, SEM_POST for up (see
            @ref identifiers.py)
            - input - the parser's input string as a tuple of
            integers/character codes
            - index - the index of the first character of the matched phrase
            - length - the number of characters in the matched phrase
            - data - the user-supplied data (see @ref Ast.translate()
        '''
        inner_add_callback(self.nodes, name, callback)

    def down(self, name):
        '''Saves an AST record as the parser traverses down through a
        node with an assigned callback function.
        @param name The rule or UDT name of the node.
        '''
        if(self.nodes[name]):
            # only keep records for rule/UDT names that have callback functions
            this_record = len(self.records)
            self.indexStack.append(this_record)
            self.records.append({
                'name': name,
                'this_record': this_record,
                'that_record': None,
                'state': id.SEM_PRE,
                'callback': self.nodes[name],
                'phrase_index': None,
                'phrase_length': None,
            })

    def up(self, name, phrase_index, phrase_length):
        '''Saves an AST record as the parser traverses up through a
        node with an assigned callback function.
        Completes the matching "down" record with the information
        that was not available during the downward traversal of the node.
        @param name The rule or UDT name of the node.
        @param phrase_index Index of the first input character of the matched phrase.
        @param phrase_length The number of input characters matched.
        '''
        if(self.nodes[name]):
            # only keep records for rule/UDT names that have callback functions
            this_record = len(self.records)
            that_record = self.indexStack.pop()
            self.records.append({
                'name': name,
                'this_record': this_record,
                'that_record': that_record,
                'state': id.SEM_POST,
                'callback': self.nodes[name],
                'phrase_index': phrase_index,
                'phrase_length': phrase_length,
            })
            self.records[that_record]['that_record'] = this_record
            self.records[that_record]['phrase_index'] = phrase_index
            self.records[that_record]['phrase_length'] = phrase_length

    def save_state(self):
        '''Saves the state of the AST. Should be called by the RNM operators
        so that the state can be restored should the branch below fail.
        The state is a list saving off the length of the list of
        records and the index stack.
        '''
        return [len(self.records), len(self.indexStack)]

    def restore_state(self, state):
        '''Restores the AST to a previously saved state.
        Should be called by the RNM operators, for example,
        if the branch below fails.
        @param state the return value of a previous call
        to @ref Ast.save_state()
        '''
        del self.records[state[0]:]
        del self.indexStack[state[1]:]

    def clear(self):
        '''Clear the AST for reuse by the parser.'''
        del self.records[0:]
        del self.indexStack[0:]

    def translate(self, data=None):
        '''Do a depth-first traversal of the AST nodes,
        calling user-supplied callback functions
        1) if a record for the node has been created and
        2) if the user has attached a callback function to the node
        with @ref Ast.add_callback().
        @param data User-supplied data which is made available to the
        callback functions but is otherwise ignored by the AST.'''
        inner_translate(self.input, self.nodes, self.records, data)
