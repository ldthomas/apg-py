''' @file examples/basics/look_ahead.py
@brief Example of using the look behind operators & and !.

A well-known non-context free language is
[L ={a<sup>n</sup>b<sup>n</sup>c<sup>n</sup> | n>0}]
(https://en.wikipedia.org/wiki/Syntactic_predicate).
It is shown there how to parse this using look ahead operators.
See also the brute-force method with UDTs, namely
hand written a code snippets to match a language phrase,
@ref examples/basics/udts.py.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.api.api import Api

title = '''Demonstrate the use of the look ahead operators.
& - the positive look ahead operator
  - succeeds on a specified phrase match
! - the negative look ahead operator
  - fails on a specified phrase match
'''
print()
print(title)

# SABNF syntax using the look ahead operators & and !
abnf_syntax = 'S = &(A !bb) 1*aa B !cc\n'
abnf_syntax += 'A = aa [A] bb\n'
abnf_syntax += 'B = bb [B] cc\n'
abnf_syntax += 'aa = "a"\n'
abnf_syntax += 'bb = "b"\n'
abnf_syntax += 'cc = "c"\n'

# construct the grammar object
api = Api()
grammar = api.generate(abnf_syntax)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    # use the grammar object to parse an input string
    # input string must be a tuple of positive integers
    parser = Parser(grammar)
    input_string = 'aaabbbccc'
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n1) Parser Result - input = "' + input_string + '"')
    print(result)
    input_string = 'aaabbbcc'
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n2) Parser Result - input = "' + input_string + '"')
    print(result)
