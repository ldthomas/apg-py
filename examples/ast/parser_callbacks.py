''' @file examples/ast/parser_callbacks.py
@brief The parser call back functions for the AST example.
'''


import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib import identifiers as id


def A_rule(cb_data):
    if(cb_data['state'] == id.MATCH):
        index = cb_data['phrase_index']
        end = index + cb_data['phrase_length']
        matched = utils.tuple_to_string(cb_data['input'][index:end])
        cb_data['user_data'].append('"' + matched + '" found by rule A')


def B_rule(cb_data):
    if(cb_data['state'] == id.MATCH):
        index = cb_data['phrase_index']
        end = index + cb_data['phrase_length']
        matched = utils.tuple_to_string(cb_data['input'][index:end])
        cb_data['user_data'].append('"' + matched + '" found by rule B')


def X_rule(cb_data):
    if(cb_data['state'] == id.MATCH):
        index = cb_data['phrase_index']
        end = index + cb_data['phrase_length']
        matched = utils.tuple_to_string(cb_data['input'][index:end])
        cb_data['user_data'].append('"' + matched + '" found by rule X')


def alt1_rule(cb_data):
    if(cb_data['state'] == id.MATCH):
        cb_data['user_data'].append('in rule alt1')


def alt2_rule(cb_data):
    if(cb_data['state'] == id.MATCH):
        cb_data['user_data'].append('in rule alt2')
