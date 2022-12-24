''' @file apg_py/api/syntax.py
@brief Parse the SABNF grammar for syntax errors.

Generate the AST for the semantic phase (@ref semantic.py)
'''
# for development debugging only
from apg_py.lib.trace import Trace


def syntax(api, strict):
    '''Parse the SABNF grammar.
    @param api The api object (@ref api.py) for the given grammar syntax.
    @param strict If True, strictly follow the ABNF conventions of RFCs 5234 & 7405
    @returns Returns a list of error, if any. Each error in the list has
    the dictionary form
        - 'line': the line number where the error occurred
        - 'index': the approximate relative index within the line
        where the error occurred
        - 'msg': as descriptive error message
    '''
    data = {}
    data['find_line'] = api.find_line
    data['strict'] = strict
    data['errors'] = []
    data['max_index'] = 0
    # Trace(api.parser, mode='xc')
    result = api.parser.parse(api.input, user_data=data)
    if(result.success is False):
        # raise Exception('Internal Error: syntax parser should never fail')
        msg = 'fatal syntax error encountered'
        msg += ' - parser stopped approximately here'
        data['errors'].append({
            'line': api.find_line(result.max_phrase_length),
            'index': result.max_phrase_length,
            'msg': msg
        })
    return data['errors']
