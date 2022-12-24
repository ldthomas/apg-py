''' @file examples/exp/csv.py
@brief Demonstrates parsing comma separated values.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp
from apg_py.lib import utilities as utils

title = '''This example will demonstrate how to parse the
Microsoft format for comma separated values.
Two approaches are compared. One is to parse out one value
at a time with repeated searches using the global flag.
The other is to parse all values out of a line in one fell swoop.
Note that some translation is required to get the values
from quoted fields.
This problem is addressed in Jeffrey Friedl's book
"Mastering Regular Expressions", pg. 213
You can compare this solution to his discussion there.
'''
print()
print(title)

csv_value = '''value         = begin-anchor field end-anchor
begin-anchor  = &&%d44 / %^
end-anchor    = &%d44 / %$
field         = quoted / text
quoted        = %d34 quoted-text %d34
quoted-text   = *(any-but-quote / double-quote)
double-quote  = 2%d34
any-but-quote = %d32-33 / %d35-126
text          = *any-but-comma
any-but-comma = %d32-43 / %d45-126
'''
csv_line = '''csv           = field *(%d44 field)
field         = quoted / text
quoted        = %d34 quoted-text %d34
quoted-text   = *(any-but-quote / double-quote)
double-quote  = 2%d34
any-but-quote = %d32-33 / %d35-126
text          = *any-but-comma
any-but-comma = %d32-43 / %d45-126
'''
input = '''Ten Thousand,10000, 2710 ,,"10,000","It's ""10 Grand"", baby",10K'''
pat = 'PATTERN'
header = 'RESULT'
testno = 0

# one value at a time
exp = ApgExp(csv_value, 'g')
testno += 1
print('\n' + str(testno) + ') One value at a time.')
print(pat)
print(csv_value)
print('input string: ' + input)
print(header)
result = exp.exec(input)
while(result):
    if(len(result.match) and result.match[0] == '"'):
        # strip leading and trailing quotes
        strip = result.match[1:-1]
        # replace double quotes
        strip = strip.replace('""', '"')
        print(strip)
    else:
        print(result.match)
    result = exp.exec(input)

# all values at once
exp = ApgExp(csv_line)
exp.include(['field'])
testno += 1
print('\n' + str(testno) + ') All values at once.')
print(pat)
print(csv_line)
print('input string: ' + input)
print(header)
result = exp.exec(input)
for rule in result.rules['field']:
    match = utils.tuple_to_string(rule)
    if(len(match) and match[0] == '"'):
        # strip leading and trailing quotes
        strip = match[1:-1]
        # replace double quotes
        strip = strip.replace('""', '"')
        print(strip)
    else:
        print(match)
