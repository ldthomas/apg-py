''' @file examples/grammar_object/main.py
@brief The main function for the save and use grammar object demonstratons.
@dir examples/grammar_object
@brief An example of saving a grammar object and using it at a future time.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from examples.grammar_object.save import save_grammar
from examples.grammar_object.use import use_grammar


def usage():
    display = 'usage: examples/grammar_object/main.py [--save | --use]\n'
    display += '       --save save the grammar object (default)\n'
    display += '       --use  use the previously used grammar object\n'
    return display


test = 'save'
if(len(sys.argv) > 1):
    if(sys.argv[1] == '--use'):
        # use the previously saved grammar object
        use_grammar()
        exit()
    if(sys.argv[1] != '--save'):
        print(usage())
        exit()

# default is to save the grammar object for future use
save_grammar()
