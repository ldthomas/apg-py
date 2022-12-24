''' @file examples/ini_file/ast_callbacks.py
@brief The AST call back functions for the ini file class.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils


def section_name(state, input, index, length, data):
    if(state == id.SEM_PRE):
        name = utils.tuple_to_string(input[index:index + length])
        if(name != data['current_section']):
            data['current_section'] = name
        if(not data['sections'].get(name)):
            data['sections'][name] = {}


def key_name(state, input, index, length, data):
    if(state == id.SEM_PRE):
        name = utils.tuple_to_string(input[index:index + length])
        if(data['current_section']):
            section = data['sections'][data['current_section']]
        else:
            section = data['global']
        key = section.get(name)
        if(not key):
            section[name] = []
        data['current_key'] = name


def value(state, input, index, length, data):
    if(state == id.SEM_POST):
        if(data['current_section']):
            section = data['sections'][data['current_section']]
        else:
            section = data['global']
        section[data['current_key']].append(data['value'])


def hex_digit(d):
    if(d >= 48 and d <= 57):
        return d - 48
    if(d >= 65 and d <= 72):
        return d - 55
    if(d >= 97 and d <= 104):
        return d - 87
    raise Exception('bad hex digit', d)


def string_eval(input):
    value = ''
    skip = 0
    for i in range(len(input)):
        if(skip):
            skip -= 1
        else:
            if(input[i] == 92):
                if(input[i + 1] == 120):
                    c = hex_digit(input[i + 2])
                    c = 16 * c + hex_digit(input[i + 3])
                    value += chr(c)
                    skip = 3
                elif(input[i + 1] == 117):
                    c = hex_digit(input[i + 2])
                    c = 16 * c + hex_digit(input[i + 3])
                    c = 16 * c + hex_digit(input[i + 4])
                    c = 16 * c + hex_digit(input[i + 5])
                    value += chr(c)
                    skip = 5
                else:
                    if(input[i + 1] == 116):
                        value += chr(0x09)
                    elif(input[i + 1] == 114):
                        value += chr(0x0D)
                    elif(input[i + 1] == 110):
                        value += chr(0x0A)
                    elif(input[i + 1] == 98):
                        value += chr(0x20)
                    else:
                        value += chr(input[i + 1])
                    skip = 1
            else:
                value += chr(input[i])
    return value


def d_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        data['value'] = string_eval(input[index:index + length])


def s_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        data['value'] = string_eval(input[index:index + length])


def string_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        data['value'] = string_eval(input[index:index + length])


def number_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        value = utils.tuple_to_string(input[index:index + length])
        data['value'] = int(value)


def true_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        data['value'] = True


def false_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        data['value'] = False


def null_value(state, input, index, length, data):
    if(state == id.SEM_PRE):
        data['value'] = None
