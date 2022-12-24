''' @file apg_py/api/scanner_callbacks.py
    @brief All of the callback functions for the scanner parser's AST.'''

from apg_py.lib import identifiers as id


def scanner_line(state, input, phrase_index, phrase_length, data):
    '''Add a line to the line catalog.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        data['invalid_count'] = 0
        data['text_length'] = 0
    else:
        data['lines'].append({
            'line_no': data['line_no'],
            'index': phrase_index,
            'length': phrase_length,
            'text_length': data['text_length'],
            'line_end': data['line_end'],
            'invalid_chars': data['invalid_count']
        })
    return id.SEM_OK


def scanner_last_line(state, input, phrase_index, phrase_length, data):
    '''Deal with a last line with no line ending.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        data['invalid_count'] = 0
        data['text_length'] = 0
    else:
        data['lines'].append({
            'line_no': data['line_no'],
            'index': phrase_index,
            'length': phrase_length,
            'text_length': data['text_length'],
            'line_end': '',
            'invalid_chars': data['invalid_count']
        })
        msg = 'last line must end with line end character(s)'
        data['errors'].append({
            'line': data['line_no'],
            'index': phrase_index + phrase_length,
            'msg': msg
        })
    return id.SEM_OK


def scanner_line_text(state, input, phrase_index, phrase_length, data):
    '''Capture the line text (integers from beginning of line to end.)
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        data['text_length'] = phrase_length
    return id.SEM_OK


def scanner_invalid(state, input, phrase_index, phrase_length, data):
    '''Handle an invalid character.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        msg = 'invalid character found: ' \
            + '\\x%02X' % (input[phrase_index])
        data['errors'].append({
            'line': data['line_no'],
            'index': phrase_index,
            'msg': msg
        })
    return id.SEM_OK


def scanner_end(state, input, phrase_index, phrase_length, data):
    '''Keep track of the current line number.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_POST):
        data['line_no'] += 1
    return id.SEM_OK


def scanner_lf(state, input, phrase_index, phrase_length, data):
    '''Recognize a line feed line ending.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        data['line_end'] = 'LF'
        if(data['strict']):
            msg = 'strict ABNF specified: ' + \
                'line end LF(\\x0A) not allowed - must use CRLF(\\x0D0A)'
            data['errors'].append({
                'line': data['line_no'],
                'index': phrase_index,
                'msg': msg
            })
    return id.SEM_OK


def scanner_cr(state, input, phrase_index, phrase_length, data):
    '''Recognize a carriage return line ending.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        data['line_end'] = 'CR'
        if(data['strict']):
            msg = 'strict ABNF specified: ' + \
                'line end CR(\\x0D) not allowed - must use CRLF(\\x0D0A)'
            data['errors'].append({
                'line': data['line_no'],
                'index': phrase_index,
                'msg': msg
            })
    return id.SEM_OK


def scanner_crlf(state, input, phrase_index, phrase_length, data):
    '''Recognize a carriage return, line feed combination line ending.
    @param state The tranlation state,
        - SEM_PRE the translation is traversing the node going down
        - SEM_POST the translation is traversing the node going up
    @param input The full tuple of input integers.
    @param phrase_index The index of the first integer in the matched phrase.
    @param phrase_length The number of integers in the matched phrase.
    @param data User data that was passed to the AST translation, if any.
    This is available for the user and is never examined, used or changed
    by the AST translator.
    '''
    if(state == id.SEM_PRE):
        data['line_end'] = 'CRLF'
    return id.SEM_OK
