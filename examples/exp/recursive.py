''' @file examples/exp/recursive.py
@brief Demonstrates using recursive rules for matching nested pairs.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp

title = '''This example will demonstrate the use of
recursive grammar rules for matching nested pairs.
Note that the begin and end of string anchors,
%^ and %$, are used so that the pattern must
match the entire string or fail.
'''
print()
print(title)

L = 'L = "("\n'
R = 'R = ")"\n'
# PM = 'match = %^ P %$\n'
PM = 'P = L P R / L R\n'
PM += L
PM += R
PG = 'match = %^ P %$\n'
PG += 'P = L 1*P R / L R\n'
PG += L
PG += R
PT = 'match = %^ P %$\n'
PT += 'P = L text 1*(P text) R / L text R\n'
PT += 'L = "<"\n'
PT += 'R = ">"\n'
PT += 'text = *(%d32-59 / %d61 / %d63-126)\n'
header = 'RESULT'
testno = 0

# simple parentheses matching
exp = ApgExp(PM)
exp.include(['P'])
input = '((()))'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Simple parethesis matching')
print('input string: ' + input)
print(header)
print(result)
input = '((())'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Simple parentheses matching - unmatched input')
print('input string: ' + input)
print(header)
print(result)

# internal pairs parentheses matching
exp = ApgExp(PG)
exp.include(['P'])
input = '(()(())())'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Internal pairs of parentheses matching.')
print('input string: ' + input)
print(header)
print(result)

# internal pairs of parentheses with text
exp = ApgExp(PT)
exp.include(['P', 'text'])
input = '<up 1<up 2< middle 1 >between<middle 2>down 2>down 1>'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Internal pairs of parentheses with text.')
print('input string: ' + input)
print(header)
print(result)
