''' @file examples/exp/split.py
@brief Demonstrates the use of the split() function.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp
from apg_py.lib import utilities as utils

title = '''This example will demonstrate how to use
the split function. This function is similar to the
JavaScript string split function
(https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split)
with a regex expression for the split pattern.
From apg/exp/exp.py
All flags except the character code flag "c" are ignored.
If the "c" flag is set, substitute "tuple of character codes" for string.
  - if the input string is empty, the output list contains
  a single empty string
  - if the pattern matches the entire string, the output list contains
  a single empty string.
  - if no pattern matches are found in the input string,
  the output list contains a single string which
  is a copy of the input string.
  - if the pattern finds multiple matches, the output list contains
  a each of the strings between the matches
  - if the pattern matches the empty string, the output will be a list
  of the single characters.
'''
print()
print(title)

pattern = 'start = %s"The entire string."\n'
pat = 'PATTERN'
header = 'RESULT'
testno = 0

# empty input string
exp = ApgExp(pattern)
input = ''
result = exp.split(input)
testno += 1
print('\n' + str(testno) + ') Empty input string.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)

# pattern matches the entire string
exp = ApgExp(pattern)
input = 'The entire string.'
result = exp.split(input)
testno += 1
print('\n' + str(testno) + ') Pattern matches the entire string.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)

# separator matches
pattern = '''pattern = wsp / (owsp "," owsp) / (owsp ";" owsp)
wsp = %d32 / %d9
owsp = *wsp
'''
exp = ApgExp(pattern)
input = 'dog cat,bird ; mouse, rabbit'
result = exp.split(input)
testno += 1
print('\n' + str(testno) + ') Multiple separator matches.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)

# separator matches with limits
pattern = '''pattern = wsp / (owsp "," owsp) / (owsp ";" owsp)
wsp = %d32 / %d9
owsp = *wsp
'''
exp = ApgExp(pattern)
input = 'dog cat,bird ; mouse, rabbit'
result = exp.split(input, limit=3)
testno += 1
print('\n' + str(testno) + ') Multiple separator matches limited to 3.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)

# separator matches with limits using characters
pattern = '''pattern = wsp / (owsp "," owsp) / (owsp ";" owsp)
wsp = %d32 / %d9
owsp = *wsp
'''
exp = ApgExp(pattern, 'c')
input = 'dog cat,bird ; mouse, rabbit'
result = exp.split(utils.string_to_tuple(input), limit=3)
testno += 1
print(
    '\n' +
    str(testno) +
    ') Multiple separator matches limited to 3 in character codes.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)

# matches the empty string
pattern = '''pattern = ""
'''
exp = ApgExp(pattern)
input = 'Separate into characters.'
result = exp.split(input)
testno += 1
print('\n' + str(testno) + ') Separate into characters with an empty string match.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)

# matches the empty string in characters
pattern = '''pattern = ""
'''
exp = ApgExp(pattern, 'c')
input = 'characters'
result = exp.split(utils.string_to_tuple(input))
testno += 1
print(
    '\n' +
    str(testno) +
    ') Separate into character codes with an empty string match.')
print(pat)
print(pattern)
print('input string: ' + input)
print(header)
print(result)
