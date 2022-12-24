''' @file examples/ini_file/parser_callbacks.py
@brief The parser call back functions for the ini file class.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import identifiers as id


def line_end(cb):
    if(cb['state'] == id.MATCH):
        cb['user_data']['line_no'] += 1


def bad_section_line(cb):
    if(cb['state'] == id.MATCH):
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': 'bad section definition'})


def bad_value_line(cb):
    if(cb['state'] == id.MATCH):
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': 'bad key/value definition'})


def bad_blank_line(cb):
    if(cb['state'] == id.MATCH):
        msg = 'invalid blank line, only white space and comments allowed'
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': msg})
