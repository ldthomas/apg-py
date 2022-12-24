''' @file examples/basics/back_reference.py
@brief Demonstrates two modes of back referencing.
    - "universal" mode - The back reference matches the last
of all previously matched phrases regardless of where on the parse
tree it occurred.
    - "recursive" mode - The back reference matches the previously
matched phrase which has the same recursive rule parent node.
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

title = '''Demonstrates back referencing.
A "universal" mode back reference matches the last
of all previous matched phrases.
A "recursive" mode back reference matches the previously
matched phrase which has the same recursive rule parent node.
'''
print()
print(title)

usyntax = '''html = "<" tag-name ">" [html] "</" \\tag-name ">"
tag-name = alpha *(alphanum)
alpha = %d97-122 / %d65-90
alphanum = alpha / %d48-57
'''
rsyntax = '''html = "<" tag-name ">" [html] "</" \\%rtag-name ">"
tag-name = alpha *(alphanum)
alpha = %d97-122 / %d65-90
alphanum = alpha / %d48-57
'''
rssyntax = '''html = "<" tag-name ">" [html] "</" \\%s%rtag-name ">"
tag-name = alpha *(alphanum)
alpha = %d97-122 / %d65-90
alphanum = alpha / %d48-57
'''

# construct the grammar object
api = Api()
grammar = api.generate(usyntax)
if(api.errors):
    # report any errors
    print('\nGrammar Errors')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    input = '<level1><level2><level3></level3></level3></level3>'
    result = parser.parse(utils.string_to_tuple(input))
    print('\n1) Universal mode - all closing tag names must be equal', end=' ')
    print('to the last level opening tag name - not correct HTML.')
    print(result)

# recursive - case insensitive
grammar = api.generate(rsyntax)
if(api.errors):
    # report any errors
    print('\nGrammar Errors')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    input = '<level1><level2><level3></Level3></LEVEL2></level1>'
    result = parser.parse(utils.string_to_tuple(input))
    print('\n2) Recursive mode - all closing tag names must be equal', end=' ')
    print('to the matching opening tag name, however, case insensitive.')
    print(result)


# recursive - case sensitive
grammar = api.generate(rssyntax)
if(api.errors):
    # report any errors
    print('\nGrammar Errors')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    input = '<level1><LEVEL2><level3></level3></LEVEL2></level1>'
    result = parser.parse(utils.string_to_tuple(input))
    print('\n2) Recursive mode - all closing tag', end=' ')
    print('names must be equal to the matching opening tag name,', end='')
    print(' case sensitive.')
    print(result)
