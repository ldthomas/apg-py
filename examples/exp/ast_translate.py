''' @file examples/exp/ast_translate.py
@brief Demonstrates using the AST for translation
 of the pattern matched results.
 Also demonstrates how to use the AST in the replace() function
 (see @ref apg/exp/exp.py.)
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.exp.exp import ApgExp
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils

title = '''This example will demonstrate how to use the AST
for matched result translations. ApgExp will be used to match
floating point numbers and the AST will be used to put the
numbers in a "normalized" form.
A second example will use the same AST to create a replacement
function to do replacements with the translated matches.
See also the examples/exp/ast.py and examples/exp/replace.py examples.
'''
print()
print(title)

# AST callback functions


def float(state, input, index, length, data):
    ret = id.SEM_OK
    if(state == id.SEM_PRE):
        data['sign'] = ''
        data['integer'] = '0'
        data['fraction'] = '0'
        data['esign'] = '+'
        data['exp'] = 0
        return ret
    if(state == id.SEM_POST):
        exponent = '' if(data['exp'] == 0) else 'e' + \
            data['esign'] + str(data['exp'])
        data['normal'] = data['sign'] + \
            data['integer'] + '.' + data['fraction'] + exponent
        return ret


def sign(state, input, index, length, data):
    ret = id.SEM_OK
    if(state == id.SEM_PRE):
        if(input[index] == 45):
            data['sign'] = '-'
    return ret


def integer(state, input, index, length, data):
    ret = id.SEM_OK
    if(state == id.SEM_PRE):
        if(length > 0):
            data['integer'] = utils.tuple_to_string(
                input[index:index + length])
    return ret


def fraction(state, input, index, length, data):
    ret = id.SEM_OK
    if(state == id.SEM_PRE):
        if(length > 0):
            data['fraction'] = utils.tuple_to_string(
                input[index:index + length])
    return ret


def esign(state, input, index, length, data):
    ret = id.SEM_OK
    if(state == id.SEM_PRE):
        if(input[index] == 45):
            data['esign'] = '-'
    return ret


def exponent(state, input, index, length, data):
    ret = id.SEM_OK
    if(state == id.SEM_PRE):
        exp = utils.tuple_to_string(input[index:index + length])
        data['exp'] = int(exp)
    return ret


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
input = '[ 123 ]'
input += '[ 123. ]'
input += '[ .123 ]'
input += '[ +.123 ]'
input += '[ -1.23 ]'
input += '[ 123.e2 ]'
input += '[ .123E+1 ]'
input += '[ -1234.56789E-10 ]'
input += '[ 123e0 ]'
input += '[ +123e-0 ]'
input += '[ -.123e-001 ]'
input += '[ 123e+000 ]'
header = 'RESULT'
testno = 0

# use the global flag to find all matches
exp = ApgExp(pattern, 'g')
exp.include(['float', 'sign', 'integer', 'fraction', 'esign', 'exp'])
result = exp.exec(input)
testno += 1
print('\n' + str(testno) + ') Normalize all matched floating point numbers.')
print('input string: ' + input)
print(header)
while(result):
    result.ast.add_callback('float', float)
    result.ast.add_callback('sign', sign)
    result.ast.add_callback('integer', integer)
    result.ast.add_callback('fraction', fraction)
    result.ast.add_callback('esign', esign)
    result.ast.add_callback('exp', exponent)
    data = {}
    result.ast.translate(data)
    print(result.match, end=' => ')
    print(data['normal'])
    result = exp.exec(input)


def fn(input, result):
    result.ast.add_callback('float', float)
    result.ast.add_callback('sign', sign)
    result.ast.add_callback('integer', integer)
    result.ast.add_callback('fraction', fraction)
    result.ast.add_callback('esign', esign)
    result.ast.add_callback('exp', exponent)
    data = {}
    result.ast.translate(data)
    return data['normal']


# replace all matches with the normalized form
testno += 1
print(
    '\n' +
    str(testno) +
    ') Use AST translation function to replace all matches with normalized form.')
print('input string: ' + input)
print(header)
result = exp.replace(input, fn)
print(result)
