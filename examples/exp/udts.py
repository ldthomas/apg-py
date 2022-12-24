''' @file examples/exp/udts.py
@brief Demonstrates using User-Defined Terminals (UDTs).
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp
from apg_py.lib import identifiers as id

title = '''This example will demonstrate how to use
handwritten code snippets to match patterns that are
difficult to describe with an SABNF grammar.
An IPv4 address is simple to describe verbally,
but the constraints on the digits are quite complicated
in the ABNF syntax. For example, with the form
xxx.xxx.xxx.xxx
xxx can be any number 0-255. However,
 - it may or may not have leading zeros
 - if three digits, the first must be <= 2
 - if 2, the second digit must be <= 5
 - if 2 and the second digit is 5 then the third must be <= 5
Straight forward verbally but not a simple ABNF problem.
Here we show a brute force the solution with a handwritten
phrase-matching terminal, an APG UDT.
'''
print()
print(title)

pattern = 'ipv4 = %^ u_digits %d46 u_digits %d46 u_digits %d46 u_digits %$\n'
print()
print('PATTERN - Note the use of anchors. Must match the entire string.')
print(pattern)
header = 'RESULT'
testno = 0


def u_digits(cb_data):
    '''A handwritten code snippet to recognize an IPv4 digit 0 - 255.'''
    digits = 0
    count = 0
    for i in range(cb_data['phrase_index'], cb_data['sub_end']):
        c = cb_data['input'][i]
        if(c < 48 or c > 57):
            # not a decimal digit
            break
        digits = 10 * digits + (c - 48)
        count += 1
        if(count == 3):
            break
    if(count > 0 and digits <= 255):
        # success
        cb_data['state'] = id.MATCH
        cb_data['phrase_length'] = count
    else:
        # failure
        cb_data['state'] = id.NOMATCH
        cb_data['phrase_length'] = 0


# the full result
exp = ApgExp(pattern)
exp.define_udts({'u_digits': u_digits})
exp.include(['u_digits'])
input = '192.168.001.1'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Valid IPv4.')
print('input string: ' + input)
print(header)
print(result)

# max
input = '255.001.01.000'
result = exp.test(input)
testno += 1
print('\n' + str(testno) + ') Max/min IPv4.')
print('input string: ' + input)
print(header)
print(result)

# bad numbers
input = '256.001.01.000'
result = exp.test(input)
testno += 1
print('\n' + str(testno) + ') Bad IPv4.')
print('input string: ' + input)
print(header)
print(result)

input = '255.255.255.300'
result = exp.test(input)
testno += 1
print('\n' + str(testno) + ') Bad IPv4.')
print('input string: ' + input)
print(header)
print(result)

input = '255.255.255'
result = exp.test(input)
testno += 1
print('\n' + str(testno) + ') Bad IPv4.')
print('input string: ' + input)
print(header)
print(result)
