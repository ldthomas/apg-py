''' @file apg_py/api/scanner.py
@brief Scans the SABNF source for invalid characters.'''
from apg_py.api.scanner_callbacks import scanner_line
from apg_py.api.scanner_callbacks import scanner_last_line
from apg_py.api.scanner_callbacks import scanner_line_text
from apg_py.api.scanner_callbacks import scanner_invalid
from apg_py.api.scanner_callbacks import scanner_end
from apg_py.api.scanner_callbacks import scanner_lf
from apg_py.api.scanner_callbacks import scanner_cr
from apg_py.api.scanner_callbacks import scanner_crlf
from apg_py.api import scanner_grammar
from apg_py.lib.parser import Parser
from apg_py.lib.ast import Ast


def scanner(input, strict):
    '''Scan the input for invalid characters and construct a line catalog
    for looking up line numbers from character indexes.
    @param input A tuple of positive integers. Often, but not necessarily,
    character codes.
    @param strict If True, only RFC 5234 line endings allowed (CRLF).
    @returns Returns a dictionary of errors, if any, and the line catalog.
    {'errors': data['errors'], 'lines': data['lines']}
    '''
    parser = Parser(scanner_grammar)
    ast = Ast(parser)
    ast.add_callback('line', scanner_line)
    ast.add_callback('last-line', scanner_last_line)
    ast.add_callback('line-text', scanner_line_text)
    ast.add_callback('invalid', scanner_invalid)
    ast.add_callback('end', scanner_end)
    ast.add_callback('lf', scanner_lf)
    ast.add_callback('cr', scanner_cr)
    ast.add_callback('crlf', scanner_crlf)
    result = parser.parse(input)
    if(result.success is False):
        # this should never happen
        msg = 'Unexpected error scanning input grammar.' \
            + ' Grammar is seriously malformed.'
        raise Exception(msg)
    data = {}
    data['strict'] = strict
    data['lines'] = []
    data['line_no'] = 0
    data['line_end'] = None
    data['errors'] = []
    ast.translate(data)
    return {'errors': data['errors'], 'lines': data['lines']}
