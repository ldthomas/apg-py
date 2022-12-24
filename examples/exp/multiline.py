''' @file examples/exp/multiline.py
@brief Demonstrates mimicking the multi-line mode flag of regex.
'''
import sys
import os
import re
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp

title = '''This example will demonstrate how to mimick
the multi-line mode flag of regex.
'''
print()
print(title)

pattern = 'line     = beg "The " animal " in the hat." end\n'
pattern += 'beg      = (&&line-end / %^) ; begin of line or preceeded by line end\n'
pattern += 'end      = (&line-end / %$)  ; followed by line end or input\n'
pattern += 'animal   = "cat" / "dog" / "bird" / "mouse"\n'
pattern += 'line-end = %d13.10 / %d10 / %d13\n'
print()
input = 'The cat in the hat.\n'
input += 'The dog in the hat.\n'
input += 'The bird in the hat.\n'
input += 'The mouse in the hat.'
header = 'RESULT'
testno = 0

# Python regex
re_pattern = r'^The (cat|dog|bird|mouse) in the hat.$'
matches = re.finditer(re_pattern, input, re.M)
testno += 1
print(str(testno) + ') Python regex with the multi-line flag, re.M, set.')
print('PATTERN: ', end='')
print(re_pattern)
print('input string:\n' + input)
print()
print(header)
for match in matches:
    print(match)


# ApgExp
exp = ApgExp(pattern, 'g')
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') The ApgExp global match.')
print('PATTERN')
print(pattern)
print('input string:\n' + input)
print()
print(header)
while(result):
    print(result.match)
    result = exp.exec(input)
