''' @file examples/basics/udts.py
@brief Example of using User-Defined Terminals (UDTs).

A well-known non-context free language is
[L ={a<sup>n</sup>b<sup>n</sup>c<sup>n</sup> | n>0}]
(https://en.wikipedia.org/wiki/Syntactic_predicate).
It is shown there how to parse this using look ahead operators
and that will be demonstrated in the look ahead example,
@ref examples/basics/look_ahead.py.
Here, we demonstrate a more brute-force method - namely
simply hand writting a code snippet to match the language.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib import identifiers as id
from apg_py.lib.parser import Parser
from apg_py.api.api import Api


def anbncn(cb_data):
    # the UDT callback function
    # default to failure - NOMATCH
    cb_data['state'] = id.NOMATCH
    cb_data['phrase_length'] = 0
    na = 0
    nb = 0
    nc = 0
    for i in range(cb_data['phrase_index'], cb_data['sub_end']):
        if(cb_data['input'][i] == 97):
            na += 1
        else:
            break
    if(na == 0):
        return
    for i in range(cb_data['phrase_index'] + na, cb_data['sub_end']):
        if(cb_data['input'][i] == 98):
            nb += 1
        else:
            break
    if(nb != na):
        return
    for i in range(cb_data['phrase_index'] + na + nb, cb_data['sub_end']):
        if(cb_data['input'][i] == 99):
            nc += 1
        else:
            break
    if(nc != na):
        return
    # success
    cb_data['state'] = id.MATCH
    cb_data['phrase_length'] = na + nb + nc


title = '''Demonstrate the use of User-Defined Terminals (UDTs).
These are handwritten code snippets for matching
difficult to express or non-context-free phrases.
'''
print()
print(title)

# the SABNF syntax
abnf_syntax = 'S = u_anbncn\n'

# construct the grammar object
api = Api()
grammar = api.generate(abnf_syntax)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    # parse a string that matches the language
    parser = Parser(grammar)
    parser.add_callbacks({'u_anbncn': anbncn})
    input_string = 'aaabbbccc'
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n1) Parser Result - input = "' + input_string + '"')
    print(result)

    # parse a string that does not match the language
    input_string = 'aaabbbcc'
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n2) Parser Result - input = "' + input_string + '"')
    print(result)
