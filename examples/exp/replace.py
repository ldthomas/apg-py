''' @file examples/exp/replace.py
@brief Demonstrates use of the replace function.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp

title = '''This example will demonstrate how replace matched
results. The replacements can be simple string replacements,
replacements with components of the result or with a custom
function for complex replacements.
'''
print()
print(title)

pattern = '''start = X / Y
X = A B C
A = "a"
B = "b"
C = "c"
Y = 'xyz'
'''
print()
print('PATTERN')
print(pattern)
header = 'RESULT'
testno = 0

# replace only the first match
exp = ApgExp(pattern)
input = '---abc___xyz+++'
repl = '555'
result = exp.replace(input, repl)
testno += 1
print('\n' + str(testno) + ') Replace only the first match.')
print('input string: ' + input)
print('replacement string: ' + repl)
print(header)
print(result)

# replace all matches
exp = ApgExp(pattern, 'g')
input = '---abc___xyz+++'
result = exp.replace(input, repl)
testno += 1
print('\n' + str(testno) + ') Replace all matches with the "g" flag.')
print('input string: ' + input)
print('replacement string: ' + repl)
print(header)
print(result)

# special replacement characters
exp = ApgExp(pattern)
input = '---abc___xyz+++'
repl = '$$-$&->555-$$'
result = exp.replace(input, repl)
testno += 1
print('\n' + str(testno) + ') Special characters $$ and $&.')
print('input string: ' + input)
print('replacement string: ' + repl)
print(header)
print(result)
repl = 'left($`)|555|right($\')'
result = exp.replace(input, repl)
testno += 1
print('\n' + str(testno) + ') Special characters $` and $\'.')
print('input string: ' + input)
print('replacement string: ' + repl)
print(header)
print(result)

# rule name matches in replacement
exp.include()
repl = '${C}-${B}-${A}'
result = exp.replace(input, repl)
testno += 1
print('\n' + str(testno) + ') Special characters ${rulename}.')
print('input string: ' + input)
print('replacement string: ' + repl)
print(header)
print(result)


def fn(input, result):
    # note rule names are case insensitive and always stored in lower case
    if(len(result.rules['A'.lower()])):
        special = '555'
    else:
        special = '666'
    return special


# complex replacement function
exp = ApgExp(pattern, 'g')
exp.include()
result = exp.replace(input, fn)
testno += 1
print('\n' + str(testno) + ') Special function for complex replacement.')
print('input string: ' + input)
print(header)
print(result)

testno += 1
print(
    '\n' +
    str(testno) +
    ') See examples/exp/ast.py for an example of using the AST for a complex replacement function.')
