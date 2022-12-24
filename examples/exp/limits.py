''' @file examples/exp/limits.py
@brief Demonstrates placing limits on the node hits and parse tree depth.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp

title = '''This example will demonstrate how to place limits
on the number of node hits and parse tree depth.
Exists to avoid the problem of "catestrophic backtracking".
Although this is not nearly as big a problem for ApgExp
as it is for regex, nonetheless, facilities exist for
limiting a runaway parser.
'''
print()
print(title)

pattern = '''float    = sign decimal exponent
sign     = ["+" / "-"]
decimal  = integer [dot fraction]
           / dot fraction
integer  = 1*%d48-57
dot      = "."
fraction = *%d48-57
exponent = ["e" esign exp]
esign    = ["+" / "-"]
exp      = 1*%d48-57
'''
print()
print('PATTERN')
print(pattern)
input = '---+1234.56789E-10==='
header = 'RESULT'
testno = 0

# the full result
exp = ApgExp(pattern)
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') The full match.')
print('input string: ' + input)
print(header)
print(result)

# limit node hits
exp = ApgExp(pattern)
exp.set_node_hits(40)
testno += 1
try:
    result = exp.exec(input)
except Exception as msg:
    print('\n' + str(testno) + ') Limited node hits - parser raises an exception.')
    print('input string: ' + input)
    print('Exception: ', end='')
    print(msg)

# limit tree depth
exp = ApgExp(pattern)
exp.set_tree_depth(5)
testno += 1
print('\n' + str(testno) + ') Limited tree depth - parser raises an exception.')
print('input string: ' + input)
try:
    result = exp.exec(input)
except Exception as msg:
    print(
        '\n' +
        str(testno) +
        ') Limited tree depth - parser raises an exception.')
    print('input string: ' + input)
    print('Exception: ', end='')
    print(msg)
