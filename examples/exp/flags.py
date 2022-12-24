''' @file examples/exp/flags.py
@brief Demonstrates using the pattern matching flags.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp
from apg_py.lib import utilities as utils

title = '''This example will demonstrate the pattern matching flags
and how they work, and specifly setting "last_index", the starting character.
- with the global flag, "g", set, repeated calls to exec() will find all matches
- with the sticky flag, "y", set, repeated calls to exec() will find all consecutive matches
- with the character code flag, "c", set, input and results are in tuples of integers rather than strings
- with the trace flag, "t", set, a parsing trace facilitates debugging patterns in input strings
'''
print()
print(title)

pattern = 'start = "abc"\n'
input_global = '---abc===ABC---'
input_sticky = '---abcABC---'
header = 'RESULT'
testno = 0

# global
exp = ApgExp(pattern, 'g')
input = input_global
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') the global flag finds all matches')
print('input string: ' + input)
while(result):
    print(header)
    print(result)
    result = exp.exec(input)

# sticky
exp = ApgExp(pattern, 'y')
exp.last_index = 3
input = input_sticky
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') the sticky flag finds all consecutive matches')
print('input string: ' + input)
while(result):
    print(header)
    print(result)
    result = exp.exec(input)

exp.last_index = 1
input = input_sticky
result = exp.exec(input)
testno += 1
print(
    '\n' +
    str(testno) +
    ') with the sticky flag the match must be at exactly last_index')
print('input string: ' + input)
print('last_index: ' + str(exp.last_index))
print(header)
print(result)

# character codes
exp = ApgExp(pattern, 'c')
input = input_global
result = exp.exec(utils.string_to_tuple(input))
testno += 1
print(
    '\n' +
    str(testno) +
    ') with the character codes flag "c" set input and results are tuples of integers')
print('input string: ' + str(utils.string_to_tuple(input)))
print(header)
print(result)

# trace
exp = ApgExp(pattern, 't')
input = input_global
testno += 1
print(
    '\n' +
    str(testno) +
    ') with the trace flag "t" a trace of the parser is displayed')
result = exp.exec(input)
print('input string: ' + input)
print(header)
print(result)
