''' @file examples/exp/rules.py
@brief Demonstrates including or excluding specific pattern rules in the result.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp

title = '''This example will demonstrate how to include
or exclude specific rule names in the result.
'''
print()
print(title)

pattern = '''phone-number    = form1 / form2 / form3
form1           = open-paren area-code close-paren office-code hyphen subscriber
form2           = area-code hyphen office-code hyphen subscriber
form3           = area-code office-code subscriber
area-code       = 3digit
office-code     = 3digit
subscriber      = 4digit
open-paren      = %d40
close-paren     = %d41
hyphen          = %d45
digit           = %d48-57
'''
print()
print('PATTERN')
print(pattern)
header = 'RESULT'
testno = 0

# the full result
exp = ApgExp(pattern)
exp.include()
input = '(999)555-1234'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Form 1 - the result with all rules.')
print('   Note the abundance of uninteresting information in the result.')
print('input string: ' + input)
print(header)
print(result)

# just the important information
exp = ApgExp(pattern)
exp.include(['area-code', 'office-code', 'subscriber'])
input = '999-555-1234'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Form 2, include only the telephone number components.')
print('input string: ' + input)
print(header)
print(result)

# use exclude()
exp = ApgExp(pattern)
exp.exclude(['open-paren', 'close-paren', 'hyphen',
            'digit', 'form1', 'form2', 'form3'])
input = '8005556666'
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Form 3 - using exclude().')
print('input string: ' + input)
print(header)
print(result)
