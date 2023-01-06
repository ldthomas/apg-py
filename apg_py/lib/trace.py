''' @file apg_py/lib/trace.py @brief Displays a trace of the parse tree.
The trace is a printed description of each
parse tree node processed by the parser.
'''

import sys
# import time
from apg_py.lib import identifiers as id

# localtime = time.asctime(time.localtime(time.time()))
# print("Print Local current time :", localtime)
# sys.stdout.write('writing to stdout\n')


class Trace():
    '''Class for tracing and displaying the progress
    of the parser through the parse tree.
    The Trace class has a copy of the Parser class and knows how to use it.
    Therefore, Trace and Parser need to remain in sync throughout
    development.'''

    def __init__(self, parser, fname=None, mode='dc', line_max=32):
        '''
        @param parser The parser to trace.
        @param fname If present, the file name to write the trace to.
        @param mode The display mode.
         - 'x' Display characters as hexadecimal digits. e.g. x2e.
         - 'xc' Display all characters 32-127 as ASCII characters,
         otherwise use hexadecimal digit display.
         - 'd' Display characters as decimal digits. e.g. 32.
         - 'dc' (default) Display all characters 32-127 as ASCII characters,
         otherwise use decimal digit display.
        @param line_max The maximum line length in characters
        for any trace line.
        '''
        self.file = sys.stdout
        if(mode not in ['x', 'xc', 'd', 'dc']):
            raise Exception('mode must be one of x, d, xc, dc: found: ', mode)
        self.mode = mode
        self.parser = parser
        parser.trace = self
        if(fname):
            self.file = open(fname, "w")
        self.line_max = line_max
        self.selectOp = {
            id.ALT: self.traceALT,
            id.CAT: self.traceCAT,
            id.REP: self.traceREP,
            id.RNM: self.traceRNM,
            id.TLS: self.traceTLS,
            id.TBS: self.traceTBS,
            id.TRG: self.traceTRG,
            id.UDT: self.traceUDT,
            id.AND: self.traceAND,
            id.NOT: self.traceNOT,
            id.BKR: self.traceBKR,
            id.BKA: self.traceBKA,
            id.BKN: self.traceBKN,
            id.ABG: self.traceABG,
            id.AEN: self.traceAEN,
        }
        self.select_mode = {
            'x': self.phrasex,
            'd': self.phrased,
            'xc': self.phrasexc,
            'dc': self.phrasedc
        }

    def __del__(self):
        '''Destructor for ensuring that the output file is closed, if any.'''
        if(self.file and self.file != sys.stdout):
            # self.file.flush()
            self.file.close()
            self.file = None

    def finish(self):
        '''Guarantee that the output file is flushed.'''
        if(self.file):
            self.file.flush()

    def set_display_length(self, max_len):
        '''Set the maximum trace line display length in characters.
        @param max_len The maximum number of characters to
        display on a line.'''
        self.line_max = max(0, max_len)

    def indent(self, n):
        '''For internal use only.'''
        ret = ''
        for i in range(n):
            ret += '.'
        return ret

    def traceALT(self, op):
        '''For internal use only.'''
        return 'ALT(' + str(len(op['children'])) + ')'

    def traceCAT(self, op):
        '''For internal use only.'''
        return 'CAT(' + str(len(op['children'])) + ')'

    def traceREP(self, op):
        '''For internal use only.'''
        rep_max = str(op['max']) if(op['max'] < id.MAX_INT) else 'inf'
        return 'REP(' + str(op['min']) + ',' + rep_max + ')'

    def traceRNM(self, op):
        '''For internal use only.'''
        rule = self.parser.rules[op['index']]
        return 'RNM(' + rule['name'] + ')'

    def traceUDT(self, op):
        '''For internal use only.'''
        udt = self.parser.udts[op['index']]
        return 'UDT(' + udt['name'] + ')'

    def traceTLS(self, op):
        '''For internal use only.'''
        tChars = min(3, len(op['string']))
        tEnd = '...' if(len(op['string']) > tChars) else ''
        display = ''
        for i in range(tChars):
            if(i > 0):
                display += ','
            display += str(op['string'][i])
        return 'TLS(' + display + tEnd + ')'

    def traceTBS(self, op):
        '''For internal use only.'''
        tChars = min(3, len(op['string']))
        tEnd = '...' if(len(op['string']) > tChars) else ''
        display = ''
        for i in range(tChars):
            if(i > 0):
                display += ','
            display += str(op['string'][i])
        return 'TBS(' + display + tEnd + ')'

    def traceTRG(self, op):
        '''For internal use only.'''
        return 'TRG(' + str(op['min']) + ',' + str(op['max']) + ')'

    def traceAND(self, op):
        '''For internal use only.'''
        return 'AND'

    def traceNOT(self, op):
        '''For internal use only.'''
        return 'NOT'

    def traceBKR(self, op):
        '''For internal use only.'''
        case = '%i'
        if(op['bkr_case'] == id.BKR_MODE_CS):
            case = '%s'
        mode = '%u'
        if(op['bkr_mode'] == id.BKR_MODE_RM):
            case = '%r'
        return 'BKR(\\' + case + mode + op['name'] + ')'

    def traceBKA(self, op):
        '''For internal use only.'''
        return 'BKA'

    def traceBKN(self, op):
        '''For internal use only.'''
        return 'BKN'

    def traceABG(self, op):
        '''For internal use only.'''
        return 'ABG'

    def traceAEN(self, op):
        '''For internal use only.'''
        return 'AEN'

    def phrasex(self, phrase):
        '''For internal use only.'''
        ret = ''
        count = 0
        for dig in phrase:
            if(count > 0):
                ret += ' '
            ret += ('x%02x' % dig)
            count += 1
        return ret

    def phrasexc(self, phrase):
        '''For internal use only.'''
        ret = ''
        count = 0
        prev_not_ascii = True
        for dig in phrase:
            if(dig >= 32 and dig < 127):
                if(count > 0 and prev_not_ascii):
                    ret += ' '
                prev_not_ascii = False
                ret += chr(dig)
            else:
                if(count > 0):
                    ret += ' '
                ret += ('x%02x' % dig)
                prev_not_ascii = True
            count += 1
        return ret

    def phrased(self, phrase):
        '''For internal use only.'''
        ret = ''
        count = 0
        for dig in phrase:
            if(count > 0):
                ret += ' '
            ret += ('%d' % dig)
            count += 1
        return ret

    def phrasedc(self, phrase):
        '''For internal use only.'''
        ret = ''
        count = 0
        prev_not_ascii = True
        for dig in phrase:
            if(dig >= 32 and dig < 127):
                if(count > 0 and prev_not_ascii):
                    ret += ' '
                prev_not_ascii = False
                ret += chr(dig)
            else:
                if(count > 0):
                    ret += ' '
                ret += ('%d' % dig)
                prev_not_ascii = True
            count += 1
        return ret

    def down(self, op):
        '''For internal use only.'''
        if(self.parser.current_look_direction == id.LOOKAROUND_BEHIND):
            arrow = '<- '
        else:
            arrow = '-> '
        fn = self.selectOp.get(op['type'])
        ret = self.indent(self.parser.tree_depth)
        ret += '|-|-|'
        ret += fn(op)
        ret += arrow
        phraseEnd = min(
            self.parser.sub_end,
            self.parser.phrase_index +
            self.line_max)
        line_end = '' if(phraseEnd == self.parser.sub_end) else '...'
        phrase = self.parser.input[
            self.parser.phrase_index:phraseEnd]
        charFormat = self.select_mode.get(self.mode, None)
        ret += charFormat(phrase)
        ret += line_end
        self.file.write(ret + '\n')

    def up(self, op, begin_index):
        '''For internal use only.'''
        state = self.parser.state
        if(self.parser.current_look_direction == id.LOOKAROUND_BEHIND):
            arrow = '<- '
            phrase_length = begin_index - self.parser.phrase_index
            display_length = min(phrase_length, self.line_max)
            phrase_index = self.parser.phrase_index
        else:
            arrow = '-> '
            phrase_length = self.parser.phrase_index - begin_index
            display_length = min(phrase_length, self.line_max)
            phrase_index = self.parser.phrase_index - phrase_length
        ret = self.indent(self.parser.tree_depth)
        stateDisplay = id.dict.get(state, None)[0]
        ret += '|' + stateDisplay + '|' + \
            str(phrase_length) + '|'
        fn = self.selectOp.get(op['type'])
        ret += fn(op)
        if(state == id.MATCH):
            ret += arrow
            line_end = '...' if(
                display_length < phrase_length) else ''
            phrase = self.parser.input[phrase_index:
                                       phrase_index + display_length]
            charFormat = self.select_mode.get(self.mode, None)
            ret += charFormat(phrase)
            ret += line_end
        elif(state == id.EMPTY):
            ret += arrow
        self.file.write(ret + '\n')
