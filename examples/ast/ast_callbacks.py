''' @file examples/ast/ast_callbacks.py
@brief The AST call back functions for the AST example.
'''


import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib import identifiers as id


def A_ast(state, input, index, length, data):
    if(state == id.SEM_PRE):
        matched = utils.tuple_to_string(input[index:index + length])
        data.append('"' + matched + '" found by AST in rule A')


def B_ast(state, input, index, length, data):
    if(state == id.SEM_PRE):
        matched = utils.tuple_to_string(input[index:index + length])
        data.append('"' + matched + '" found by AST in rule B')


def X_ast(state, input, index, length, data):
    if(state == id.SEM_PRE):
        matched = utils.tuple_to_string(input[index:index + length])
        data.append('"' + matched + '" found by AST in rule X')


def alt1_ast(state, input, index, length, data):
    if(state == id.SEM_POST):
        matched = utils.tuple_to_string(input[index:index + length])
        data.append('"' + matched + '" found by AST in rule ast1')


def alt2_ast(state, input, index, length, data):
    if(state == id.SEM_POST):
        matched = utils.tuple_to_string(input[index:index + length])
        data.append('"' + matched + '" found by AST in rule ast2')
