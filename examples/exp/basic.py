''' @file examples/exp/basic.py
@brief Demonstrates simple matching and testing of patterns in a string.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp

title = '''This example will demonstrate the basic procedure
for matching a pattern in a string and simply
testing to see if the pattern exists.
Note that specifying case insensitive matching is done
with the SABNF pattern, not with flags, as in regex.
'''
print()
print(title)

pattern_ci = 'start = "abc"\n'
pattern_cs = 'start = %s"abc"\n'
input_lower = '---abc==='
input_upper = '---ABC==='
header = 'RESULT'
testno = 0

# case insensitive matching
exp = ApgExp(pattern_ci)
result = exp.exec(input_lower)
testno += 1
print('\n' + str(testno) + ') Case insensitive - match the lower case pattern')
print('input string: ' + input_lower)
print(header)
print(result)
result = exp.exec(input_upper)
testno += 1
print('\n' + str(testno) + ') Case insensitive - match the upper case pattern')
print('input string: ' + input_upper)
print(header)
print(result)

# case insensitive testing
exp = ApgExp(pattern_ci)
result = exp.test(input_lower)
testno += 1
print('\n' + str(testno) + ') Case insensitive - test the lower case pattern')
print('input string: ' + input_lower)
print(header)
print(result)
result = exp.test(input_upper)
testno += 1
print('\n' + str(testno) + ') Case insensitive - test the upper case pattern')
print('input string: ' + input_upper)
print(header)
print(result)

# case sensitive matching
exp = ApgExp(pattern_cs)
result = exp.exec(input_lower)
testno += 1
print('\n' + str(testno) + ') Case sensitive - match the lower case pattern')
print('input string: ' + input_lower)
print(header)
print(result)
exp = ApgExp(pattern_cs)
result = exp.exec(input_upper)
testno += 1
print('\n' + str(testno) + ') Case sensitive - match the upper case pattern')
print('input string: ' + input_upper)
print(header)
print(result)

# case sensitive testing
exp = ApgExp(pattern_cs)
result = exp.test(input_lower)
testno += 1
print('\n' + str(testno) + ') Case sensitive - test the lower case pattern')
print('input string: ' + input_lower)
print(header)
print(result)
result = exp.test(input_upper)
testno += 1
print('\n' + str(testno) + ') Case sensitive - test the upper case pattern')
print('input string: ' + input_upper)
print(header)
print(result)
