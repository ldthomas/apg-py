''' @file examples/ast/main.py
@brief Example of using the Abstract Syntax Tree (AST).
The AST can be considered a sub-tree of the full parse tree.
It only has nodes for named phrases (rule name and UDT name).
The user has control over which rule and UDT names to retain on the AST
and the parser only retains those nodes with successful phrase matches.
This means that when traversing the AST, as opposed to the full
parse tree during parsing, only named nodes of interest are encountered
and the matched phrase is available in both the downward and upward directions.
This avoids reporting information from rules that are matched but exist
on parse tree branches that ultimately fail.
@dir examples/ast All of the files for the AST demonstration.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.ast import Ast
from apg_py.api.api import Api
import examples.ast.ast_callbacks as ast_callbacks
import examples.ast.parser_callbacks as parser_callbacks


title = '''Demonstrate the use of the Abstract Syntax Tree.
Demonstrates how to use the AST and why it is useful.
'''
print()
print(title)

abnf_syntax = 'S = alt1 / alt2\n'
abnf_syntax += 'alt1 = X A\n'
abnf_syntax += 'alt2 = X B\n'
abnf_syntax += 'X = "xyz"\n'
abnf_syntax += 'A = "aaa"\n'
abnf_syntax += 'B = "bbb"\n'
print()
print('the ABNF grammar syntax')
print(abnf_syntax)

# construct the grammar object
api = Api()
grammar = api.generate(abnf_syntax)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    # translations done with rule callback functions
    parser = Parser(grammar)
    parser.add_callbacks({'A': parser_callbacks.A_rule,
                         'B': parser_callbacks.B_rule,
                          'X': parser_callbacks.X_rule})
    parser.add_callbacks(
        {'alt1': parser_callbacks.alt1_rule,
         'alt2': parser_callbacks.alt2_rule})
    data = []
    input_string = 'xyzbbb'
    result = parser.parse(utils.string_to_tuple(input_string), user_data=data)
    print('\n1) Rule Translation Result - input = "' + input_string + '"')
    for string in data:
        print(string)
    print('NOTE: "xyz" found in rule X twice because', end=' ')
    print('the rule alt1 failed afer rule X succeeded.')
    data = []
    input_string = 'xyzaaa'
    result = parser.parse(utils.string_to_tuple(input_string), user_data=data)
    print('\n2) Rule Translation Result - input = "' + input_string + '"')
    for string in data:
        print(string)

    # translations done with AST callback functions
    parser = Parser(grammar)
    ast = Ast(parser)
    ast.add_callback('A', ast_callbacks.A_ast)
    ast.add_callback('B', ast_callbacks.B_ast)
    ast.add_callback('X', ast_callbacks.X_ast)
    ast.add_callback('alt1', ast_callbacks.alt1_ast)
    ast.add_callback('alt2', ast_callbacks.alt2_ast)
    data = []
    input_string = 'xyzbbb'
    result = parser.parse(utils.string_to_tuple(input_string))
    ast.translate(data)
    print('\n3) AST Translation Result - input = "' + input_string + '"')
    for string in data:
        print(string)
    data = []
    input_string = 'xyzaaa'
    result = parser.parse(utils.string_to_tuple(input_string))
    ast.translate(data)
    print('\n4) AST Translation Result - input = "' + input_string + '"')
    for string in data:
        print(string)
