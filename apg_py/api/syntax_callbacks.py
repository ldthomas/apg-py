''' @file apg_py/api/syntax_callbacks.py
@brief All the syntax parser's callback functions.
'''
from apg_py.lib import identifiers as id


def add_syntax_callbacks(parser):
    parser.add_callbacks({'rule': syntax_rule_error})
    parser.add_callbacks({'rule-name': syntax_rule_name_error})
    parser.add_callbacks({'equals': syntax_defined_as_error})
    parser.add_callbacks({'group-close': syntax_group_close_error})
    parser.add_callbacks({'option-close': syntax_option_close_error})
    parser.add_callbacks({'tls-close': syntax_tls_close_error})
    parser.add_callbacks({'cls-close': syntax_cls_close_error})
    parser.add_callbacks({'string-tab': syntax_string_tab})
    parser.add_callbacks({'pros-val': syntax_pros_val})
    parser.add_callbacks({'pros-val-close': syntax_pros_val_close_error})
    parser.add_callbacks({'udt-op': syntax_udt_op})
    parser.add_callbacks({'and-op': syntax_and_op})
    parser.add_callbacks({'not-op': syntax_not_op})
    parser.add_callbacks({'bkr-op': syntax_bkr_op})
    parser.add_callbacks({'bka-op': syntax_bka_op})
    parser.add_callbacks({'bkn-op': syntax_bkn_op})
    parser.add_callbacks({'abg-op': syntax_abg_op})
    parser.add_callbacks({'aen-op': syntax_aen_op})


def append_error(user_data, index, msg):
    user_data['errors'].append({
        'line': user_data['find_line'](index),
        'index': index,
        'msg': msg
    })


def syntax_rule_error(data):
    if(data['state'] is id.NOMATCH):
        msg = 'malformed rule (^ indicates approximate error location)'
        append_error(data['user_data'], data['max_phrase_length'], msg)


def syntax_rule_name_error(data):
    if(data['state'] is id.NOMATCH):
        msg = 'malformed rule name'
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_defined_as_error(data):
    if(data['state'] is id.NOMATCH):
        msg = 'expected "defined as"(=/ or =) not found'
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_group_close_error(data):
    if(data['state'] is id.NOMATCH):
        msg = 'expected group closure, ")", not found'
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_option_close_error(data):
    if(data['state'] is id.NOMATCH):
        msg = 'expected option closure, "]", not found'
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_tls_close_error(data):
    if(data['state'] == id.NOMATCH):
        msg = 'expected literal string closure, ", not found'
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_cls_close_error(data):
    if(data['state'] == id.NOMATCH):
        msg = "expected case-sensitive literal string closure, ', not found"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_string_tab(data):
    if(data['state'] == id.MATCH):
        msg = "tab characters not allowed in quoted strings or prose values"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_pros_val(data):
    if(data['state'] == id.MATCH):
        msg = "prose values are valid ABNF syntax but "
        msg += "but no parser operator can be generated"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_pros_val_close_error(data):
    if(data['state'] == id.NOMATCH):
        msg = "expected prose value closure, >, not found"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_udt_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "UDTs (User Defined Terminals, u_name & e_name) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_and_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "& operator (postive look ahead) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_not_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "! operator (negative look ahead) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_bkr_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "\\ operator (back referencing) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_bka_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "&& operator (positive look behind) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_bkn_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "!! operator (negative look behind) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_abg_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "%^ operator (begin of input anchor) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)


def syntax_aen_op(data):
    if(data['state'] is id.MATCH and data['user_data']['strict'] is True):
        msg = "%$ operator (end of input anchor) not allowed "
        msg += "with strict ABNF"
        append_error(data['user_data'], data['phrase_index'], msg)
