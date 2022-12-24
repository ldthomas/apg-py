''' @file examples/grammar_object/save.py
@brief Demonstrates how to save a grammar object for future use.

For grammars that are used often,
saving the grammar object prevents the repeated and redundant
re-generation of the grammar object from the SABNF syntax over and over.

Follow this with examples/grammar_object/use.py for a demonstration
of how to use this saved grammar object.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.api.api import Api


def save_grammar():
    title = '''Demonstrate how to save a grammar object to a file for later use.
The saved grammar object will be used in the companion example,
examples/grammar_object/main.py --use
'''
    print()
    print(title)

    syntax = 'abnf = tls / tbs/ trg\n'
    syntax += 'tls = "A" "B"\n'
    syntax += 'tbs = %d67.68\n'
    syntax += 'trg = 1*%d128-255\n'
    save_file = 'examples/grammar_object/abnf.py'
    api = Api()
    api.generate(syntax)
    if(api.errors):
        # report any errors
        print('\n1) Grammar Errors')
        print(api.display_errors())
    else:
        # save the grammar object for use with example
        # examples/use_grammar_object.py
        api.write_grammar(save_file)
        print('grammar saved to file ' + save_file)
        print('this file will be used by the example, examples/use_grammar_object.py')
