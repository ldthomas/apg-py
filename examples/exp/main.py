''' @file examples/exp/main.py
@brief Driver function for demonstrating a large set of
pattern matching examples.
Execute
> python3 %examples/exp/main.py --help
to see all examples.
@dir examples/exp A large set of examples of using the pattern-matching engine.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())


def usage():
    display = 'usage: python3 examples/exp/main.py option\n'
    display += '       option must be one of the following\n'
    display += '       -h, --help      display this help screen\n'
    display += '       --ast           demostrate using the AST for complex translations\n'
    display += '       --basic         demonstrates basic matching and testing a pattern\n'
    display += '       --csv           matching fields in Microsoft\'s Comma Separated Value(CSV) format\n'
    display += '       --flags         demonstrates the use of all flags, "cgyt"\n'
    display += '       --limits        setting limits on the number of node hits and parse tree depth\n'
    display += '       --multiline     how to handle the multi-line mode of regex\n'
    display += '       --recursive     matching pairs of parentheses - recursive patterns\n'
    display += '       --replace       demonstrates the use of the replace function\n'
    display += '       --rules         demonstrates capturing the phrases for specific rule names\n'
    display += '       --split         demonstrates the use of the split function\n'
    display += '       --udts          demonstrates the use of User-Defined Terminals (hand-written code snippets)\n'
    return display


if(len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    print(usage())
    exit()

if(sys.argv[1] == '--ast'):
    import examples.exp.ast_translate
    exit()

if(sys.argv[1] == '--basic'):
    import examples.exp.basic
    exit()

if(sys.argv[1] == '--csv'):
    import examples.exp.csv
    exit()

if(sys.argv[1] == '--flags'):
    import examples.exp.flags
    exit()

if(sys.argv[1] == '--limits'):
    import examples.exp.limits
    exit()

if(sys.argv[1] == '--multiline'):
    import examples.exp.multiline
    exit()

if(sys.argv[1] == '--recursive'):
    import examples.exp.recursive
    exit()

if(sys.argv[1] == '--replace'):
    import examples.exp.replace
    exit()

if(sys.argv[1] == '--rules'):
    import examples.exp.rules
    exit()

if(sys.argv[1] == '--split'):
    import examples.exp.split
    exit()

if(sys.argv[1] == '--udts'):
    import examples.exp.udts
    exit()

print('argument ' + sys.argv[1] + ' not recognized')
print(usage())
