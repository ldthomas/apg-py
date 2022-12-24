''' @file examples/grammar_object/use.py
@brief Demonstrates how to use a saved a grammar object.

For grammars that are used often,
saving the grammar object prevents the repeated and redundant
re-generation of the grammar object from the SABNF syntax over and over.

This example must be preceeded by examples/grammar_object/save.py.
This example uses the saved object from that example.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib.parser import Parser
import examples.grammar_object.abnf as grammar


def use_grammar():
    title = '''Demonstrate how to use a saved grammar object.
Uses the grammar object saved by the companion example,
save_grammar_object.py.
'''
    print()
    print(title)
    # display the original grammar
    print('the ABNF syntax of the previously saved grammar object, ', end='')
    print('examples/abnf.py')
    print(grammar.to_string())

    # construct a parser and parse a string
    parser = Parser(grammar)
    result = parser.parse((128, 200, 255))
    print(result)
