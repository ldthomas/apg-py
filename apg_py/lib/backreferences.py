''' @file apg_py/lib/backreferences.py
@brief Back reference stack class

Used for both universal and recursive back referencing.'''


class BackrefenceStack:

    def __init__(self, names):
        '''BackreferenceStack constructor.
        Creates an (empty) LIFO stack of captured phrases,
        one for each named rule or UDT.
        @param names A tuple of lower case names of all rules
        and UDTs capturing phrases for back referencing.
        '''
        self.stack = {}
        self.names = names
        for name in names:
            self.stack[name] = []

    def save_phrase(self, name, offset, length):
        '''Pushes a phrase on the named stack.
        @param name The (lower case) rule or UDT name that captured the phrase.
        @param offset The offset into the input string for the first character
        of the phrase.
        @param length The number of characters in the phrase.
        '''
        assert(name in self.names)
        self.stack[name].append([offset, length])

    def get_phrase(self, name):
        '''Retrieves the last phrase on the named stack.
        @param name The (lower case) rule or UDT name that captured the phrase.
        @returns Returns the last saved named phrase or None if none.
        '''
        assert(self.stack[name])
        length = len(self.stack[name])
        if(length):
            return self.stack[name][length - 1]
        return None

    def save_state(self):
        '''Save the stack state.
        @returns Returns a list of the named stack lengths.
        '''
        state = []
        for name in self.names:
            state.append(len(self.stack[name]))
        return state

    def restore_state(self, state):
        '''Restores all named stack lengths to a previously saved state.
        @param state The return value from a previous call
        to @ref save_state().
        '''
        i = 0
        for name in self.names:
            del self.stack[name][state[i]:]
            i += 1
