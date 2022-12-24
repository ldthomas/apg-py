''' @file examples/basics/main.py
@brief Driver function for demonstrating Python APG basic operations.
Run
<pre>python3 examples/basic/main.py --help</pre>
to see all of the basic options.
@dir examples
@brief Examples of using all aspects of the parser, parser generator
and pattern-matching engine.
In each sub-directory has a "main.py" file. Execute this file
to run the example. e.g. from your project directory
<pre>python3 examples/basic/main.py --help</pre>
will give all of the basic example options.
Examine any of the other files in the directory to study the examples
or run them in a debugger to further understand the examples lessons.
@dir examples/basics
@brief All of the examples of basic parsing operations.
Run
<pre>python3 examples/basic/main.py --help</pre>
to see all of the basic options.
Examine any of the other files in the directory to study the examples
or run them in a debugger to further understand the examples lessons.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())


def usage():
    display = 'usage: python3 examples/basics/main.py option\n'
    display += '       option must be one of the following\n'
    display += '       --back_reference demonstrates back referencing\n'
    display += '       --look_ahead     demonstrates use of look ahead operators, & and !\n'
    display += '       --look_behind    demonstrates use of look behind operators, && and !!\n'
    display += '       --parser         demonstrates basic grammar generation and parsing\n'
    display += '       --stats          demonstrates displaying the parser\'s statistics\n'
    display += '       --substrings     demonstrates parsing a substring of the full input string\n'
    display += '       --trace          demonstrated displaying a trace of the parser\'s parse tree\n'
    display += '       --udts           demonstrates the use of User_Defined Terminals, handwritten phrase matching\n'
    return display


if(len(sys.argv) == 1):
    print(usage())
    exit()

if(sys.argv[1] == '--parser'):
    import examples.basics.parsing_basics
    exit()

if(sys.argv[1] == '--back_reference'):
    import examples.basics.back_reference
    exit()

if(sys.argv[1] == '--look_ahead'):
    import examples.basics.look_ahead
    exit()

if(sys.argv[1] == '--look_behind'):
    import examples.basics.look_behind
    exit()

if(sys.argv[1] == '--stats'):
    import examples.basics.stats
    exit()

if(sys.argv[1] == '--trace'):
    import examples.basics.trace
    exit()

if(sys.argv[1] == '--substrings'):
    import examples.basics.substrings
    exit()

if(sys.argv[1] == '--udts'):
    import examples.basics.udts
    exit()

print(usage())
