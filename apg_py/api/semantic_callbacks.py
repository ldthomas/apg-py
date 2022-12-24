''' @file apg_py/api/semantic_callbacks.py
@brief All the semantic AST translation callback functions.
'''
import sys
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils


def add_ast_callbacks(ast):
    ast.add_callback('file', semantic_file)
    ast.add_callback('rule', semantic_rule)
    ast.add_callback('rule-lookup', semantic_rule_lookup)
    ast.add_callback('rule-name', semantic_rule_name)
    ast.add_callback('defined', semantic_defined)
    ast.add_callback('inc-alt', semantic_inc_alt)
    ast.add_callback('alternation', semantic_alternation)
    ast.add_callback('concatenation', semantic_concatenation)
    ast.add_callback('repetition', semantic_repetition)
    ast.add_callback('option-open', semantic_option_open)
    ast.add_callback('rep-op', semantic_rep_op)
    ast.add_callback('rep-min', semantic_rep_min)
    ast.add_callback('rep-max', semantic_rep_max)
    ast.add_callback('rep-min-max', semantic_rep_min_max)
    ast.add_callback('and-op', semantic_and_op)
    ast.add_callback('not-op', semantic_not_op)
    ast.add_callback('rnm-op', semantic_rnm_op)
    ast.add_callback('abg-op', semantic_abg_op)
    ast.add_callback('aen-op', semantic_aen_op)
    ast.add_callback('bka-op', semantic_bka_op)
    ast.add_callback('bkn-op', semantic_bkn_op)
    ast.add_callback('ci', semantic_ci)
    ast.add_callback('cs', semantic_cs)
    ast.add_callback('um', semantic_um)
    ast.add_callback('rm', semantic_rm)
    ast.add_callback('bkr-name', semantic_bkr_name)
    ast.add_callback('bkr-op', semantic_bkr_op)
    ast.add_callback('udt-empty', semantic_udt_empty)
    ast.add_callback('udt-non-empty', semantic_udt_non_empty)
    ast.add_callback('tls-op', semantic_tls_op)
    ast.add_callback('tls-string', semantic_tls_string)
    ast.add_callback('cls-string', semantic_cls_string)
    ast.add_callback('tbs-op', semantic_tbs_op)
    ast.add_callback('d-string', semantic_d_string)
    ast.add_callback('b-string', semantic_b_string)
    ast.add_callback('x-string', semantic_x_string)
    ast.add_callback('trg-op', semantic_trg_op)
    ast.add_callback('dmin', semantic_dmin)
    ast.add_callback('bmin', semantic_bmin)
    ast.add_callback('xmin', semantic_xmin)
    ast.add_callback('xmax', semantic_xmax)
    ast.add_callback('bmax', semantic_bmax)
    ast.add_callback('dmax', semantic_dmax)


def decnum(chars, beg, len):
    num = 0
    for i in range(beg, beg + len):
        num = 10 * num + chars[i] - 48
    return num


def binnum(chars, beg, len):
    num = 0
    for i in range(beg, beg + len):
        num = 2 * num + chars[i] - 48
    return num


def hexnum(chars, beg, len):
    num = 0
    for i in range(beg, beg + len):
        digit = chars[i]
        if(digit >= 48 and digit <= 57):
            digit -= 48
        elif(digit >= 65 and digit <= 70):
            digit -= 55
        elif(digit >= 97 and digit <= 102):
            digit -= 87
        else:
            raise Exception(
                'semantic-callbacks: hexnum: hex digit out of range', digit)
        num = 16 * num + digit
    return num


def semantic_file(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        # data['errors'].append({"line": 0, 'index': 0, 'msg': 'file: test'})
        data['alt_stack'] = []
        data['top_alt'] = None
        data['top_rule'] = None
        data['definedas'] = None
        data['rule_name'] = None
        data['min'] = None
        data['max'] = None
        data['top_rep'] = None
        data['ci'] = None
        data['cs'] = None
        data['um'] = None
        data['ur'] = None
        data['bkr_name'] = None
        data['tbs_str'] = None
    else:
        for rule in data['rules']:
            for op in rule['opcodes']:
                # validate RNM rule names and reset the opcode rule index
                if(op['type'] == id.RNM):
                    name = op['index']['name']
                    ph = op['index']['phrase_index']
                    lookup = data['rule_names'].get(name)
                    if(lookup == -1):
                        op['index'] = -1
                        msg = 'rule name \'' + name + '\' used but not defined'
                        data['errors'].append({
                            'line': data['find_line'](ph),
                            'index': ph,
                            'msg': msg})
                    else:
                        op['index'] = lookup['index']
                if(op['type'] == id.BKR):
                    name = op['name']['name']
                    um = op['bkr_mode'] == id.BKR_MODE_UM
                    ph = op['name']['phrase_index']
                    op['name'] = name
                    op['is_udt'] = False
                    op['empty'] = None
                    lookup = data['rule_names'].get(name)
                    if(lookup == -1):
                        # not a rule name, try UDTs
                        lookup = data['udt_names'].get(name)
                        if(lookup == -1):
                            # not a rule or UDT name
                            op['name'] = ''
                            msg = 'back referenced name \'' + name + \
                                '\' not a rule or UDT name'
                            data['errors'].append({
                                'line': data['find_line'](ph),
                                'index': ph,
                                'msg': msg})
                        else:
                            # BKR references a UDT name
                            udt = data['udts'][lookup['index']]
                            op['is_udt'] = True
                            op['empty'] = udt['empty']
                            op['index'] = udt['index']
                            if(um):
                                udt['is_bkru'] = True
                            else:
                                udt['is_bkrr'] = True
                    else:
                        ru = data['rules'][lookup['index']]
                        op['index'] = lookup['index']
                        if(um):
                            ru['is_bkru'] = True
                        else:
                            ru['is_bkrr'] = True
    return id.SEM_OK


def semantic_rule_lookup(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        if(data['definedas'] == '='):
            rule_name = data['rule_names'].add(data['rule_name'])
            if(rule_name == -1):
                # rule previously defined
                msg = 'Rule name \'' + \
                    data['rule_name'] + '\' previously defined.'
                data['errors'].append({'line': data['find_line'](phrase_index),
                                       'index': phrase_index,
                                       'msg': msg})
            else:
                # start a new rule
                data['top_rule'] = {'name': rule_name['name'],
                                    'lower': rule_name['lower'],
                                    'index': rule_name['index'],
                                    'line': data['find_line'](phrase_index),
                                    'is_bkru': False,
                                    'is_bkrr': False,
                                    'has_bkrr': False,
                                    'opcodes': []}
                data['rules'].append(data['top_rule'])
        else:
            rule_name = data['rule_names'].get(data['rule_name'])
            if(rule_name == -1):
                # rule not previously defined
                msg = 'Rule name \'' + \
                    data['rule_name'] + \
                    '\' for incremental alternative not previously defined.'
                data['errors'].append({'line': data['find_line'](phrase_index),
                                       'index': phrase_index,
                                       'msg': msg})
            else:
                data['top_rule'] = data['rules'][rule_name['index']]
    return id.SEM_OK


def semantic_rule(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['alt_stack'].clear()
        data['top_stack'] = None
    return id.SEM_OK


def semantic_rule_name(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['rule_name'] = utils.tuple_to_string(
            input[phrase_index:phrase_index + phrase_length])
    return id.SEM_OK


def semantic_defined(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['definedas'] = '='
    return id.SEM_OK


def semantic_inc_alt(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['definedas'] = '=/'
    return id.SEM_OK


def semantic_alternation(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        if(data['top_stack'] is None):
            if(data['definedas'] == '='):
                # first ALT of new rule
                data['top_alt'] = {
                    'alt': {
                        'type': id.ALT,
                        'children': []},
                    'cat': None}
                data['alt_stack'].append(data['top_alt'])
                data['top_rule']['opcodes'].append(data['top_alt']['alt'])
            else:
                # reset the rule we are adding the ALT op to
                assert(data['definedas'] == '=/'), 'invalid defined-as'
                data['top_alt'] = {
                    'alt': data['top_rule']['opcodes'][0], 'cat': None}
                data['alt_stack'].append(data['top_alt'])
        else:
            # add another ALT op to the current rule
            data['top_alt'] = {
                'alt': {
                    'type': id.ALT,
                    'children': []},
                'cat': None}
            data['alt_stack'].append(data['top_alt'])
            data['top_rule']['opcodes'].append(data['top_alt']['alt'])
    else:
        assert(state == id.SEM_POST), 'invalid AST translation state'
        # pop the ALT stack
        data['alt_stack'].pop()
        if(len(data['alt_stack']) > 0):
            data['top_alt'] = data['alt_stack'][-1]
        else:
            data['top_alt'] = None
    return id.SEM_OK


def semantic_concatenation(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['top_alt']['alt']['children'].append(
            len(data['top_rule']['opcodes']))
        data['top_alt']['cat'] = {'type': id.CAT, 'children': []}
        data['top_rule']['opcodes'].append(data['top_alt']['cat'])
    else:
        assert(state == id.SEM_POST), 'invalid AST translation state'
        data['top_alt']['cat'] = None
    return id.SEM_OK


def semantic_repetition(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['top_alt']['cat']['children'].append(
            len(data['top_rule']['opcodes']))
    return id.SEM_OK


def semantic_option_open(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['top_rule']['opcodes'].append(
            {'type': id.REP, 'min': 0, 'max': 1})
    return id.SEM_OK


def semantic_rep_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['min'] = 0
        data['max'] = sys.maxsize
        data['top_rep'] = {'type': id.REP, 'min': 0, 'max': sys.maxsize}
        data['top_rule']['opcodes'].append(data['top_rep'])
    else:
        assert(state == id.SEM_POST), 'invalid AST translation state'
        if(data['min'] > data['max']):
            min = str(data['min'])
            max = str(data['max'])
            msg = 'repetition min(' + min + ') > max(' + max + ')'
            data['errors'].append({'line': data['find_line'](phrase_index),
                                   'index': phrase_index, 'msg': msg})
        if(data['min'] == 0 and data['max'] == 0):
            msg = 'repetition 0*0 not allowed - '
            msg += 'for explicit empty string use ""'
            data['errors'].append({'line': data['find_line'](phrase_index),
                                   'index': phrase_index, 'msg': msg})
        data['top_rep']['min'] = data['min']
        data['top_rep']['max'] = data['max']
    return id.SEM_OK


def semantic_rep_min(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['min'] = decnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_rep_max(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['max'] = decnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_rep_min_max(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['max'] = decnum(input, phrase_index, phrase_length)
        data['min'] = data['max']
    return id.SEM_OK


def semantic_and_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['top_rule']['opcodes'].append({'type': id.AND, })
    return id.SEM_OK


def semantic_not_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['top_rule']['opcodes'].append({'type': id.NOT, })
    return id.SEM_OK


def semantic_rnm_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        # note: saving rule name in 'index',
        # will be converted to integer index later
        name = utils.tuple_to_string(
            input[phrase_index:phrase_index + phrase_length])
        data['top_rule']['opcodes'].append({
            'type': id.RNM,
            'index': {'name': name, 'phrase_index': phrase_index}})
    return id.SEM_OK


def semantic_abg_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['top_rule']['opcodes'].append({'type': id.ABG, })
    return id.SEM_OK


def semantic_aen_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['top_rule']['opcodes'].append({'type': id.AEN, })
    return id.SEM_OK


def semantic_bka_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['top_rule']['opcodes'].append({'type': id.BKA, })
    return id.SEM_OK


def semantic_bkn_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['top_rule']['opcodes'].append({'type': id.BKN, })
    return id.SEM_OK


def semantic_ci(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['ci'] = True
        data['cs'] = False
    return id.SEM_OK


def semantic_cs(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['cs'] = True
        data['ci'] = False
    return id.SEM_OK


def semantic_um(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['um'] = True
    return id.SEM_OK


def semantic_rm(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['ur'] = True
    return id.SEM_OK


def semantic_bkr_name(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        # phrase_index will be used for error reporting, then deleted
        name = utils.tuple_to_string(
            input[phrase_index:phrase_index + phrase_length])
        data['bkr_name'] = {'name': name, 'phrase_index': phrase_index}
    return id.SEM_OK


def semantic_bkr_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        # set defaults
        data['ci'] = True
        data['cs'] = False
        data['um'] = True
        data['ur'] = False
    else:
        assert(state == id.SEM_POST), 'invalid AST translation state'
        case = id.BKR_MODE_CS if(data['cs']) else id.BKR_MODE_CI
        mode = id.BKR_MODE_RM if(data['ur']) else id.BKR_MODE_UM
        data['top_rule']['opcodes'].append({
            'type': id.BKR,
            'name': data['bkr_name'],
            'lower': data['bkr_name']['name'].lower(),
            'bkr_case': case,
            'bkr_mode': mode
        })
    return id.SEM_OK


def generic_udt(input, phrase_index, phrase_length, data, empty=False):
    name = utils.tuple_to_string(
        input[phrase_index:phrase_index + phrase_length])
    udt_name = data['udt_names'].add(name)
    if(udt_name == -1):
        # name already exists
        udt_name = data['udt_names'].get(name)
        assert(udt_name != -1), 'UDT name list look up error'
    else:
        # add the new UDT to the UDT list
        data['udts'].append({
            'name': udt_name['name'],
            'lower': udt_name['lower'],
            'index': udt_name['index'],
            'is_bkru': False,
            'is_bkrr': False,
            'empty': empty
        })
    data['top_rule']['opcodes'].append({
        'type': id.UDT,
        'empty': empty,
        'index': udt_name['index']
    })


def semantic_udt_empty(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        generic_udt(
            input,
            phrase_index,
            phrase_length,
            data,
            empty=True)
    return id.SEM_OK


def semantic_udt_non_empty(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        generic_udt(
            input,
            phrase_index,
            phrase_length,
            data,
            empty=False)
    return id.SEM_OK


def semantic_tls_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['ci'] = True
        data['cs'] = False
    return id.SEM_OK


def semantic_tls_string(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        tup = input[phrase_index:phrase_index + phrase_length]
        if(data['ci']):
            # case insensitive (TLS)
            string = utils.tuple_to_string(tup)
            tup = utils.string_to_tuple(string.lower())
            data['top_rule']['opcodes'].append({
                'type': id.TLS,
                'string': tup
            })
        else:
            # case sensitive (TBS)
            data['top_rule']['opcodes'].append({
                'type': id.TBS,
                'string': tup
            })
    return id.SEM_OK


def semantic_cls_string(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        tup = input[phrase_index:phrase_index + phrase_length]
        if(len(tup) == 0):
            # only TLS allowed to be empty
            data['top_rule']['opcodes'].append({
                'type': id.TLS,
                'string': ''
            })
        else:
            # convert string to tuple of character codes
            data['top_rule']['opcodes'].append({
                'type': id.TBS,
                'string': tup
            })
    return id.SEM_OK


def semantic_tbs_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['tbs_str'] = []
    else:
        data['top_rule']['opcodes'].append({
            'type': id.TBS,
            'string': tuple(data['tbs_str'])
        })
    return id.SEM_OK


def semantic_d_string(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['tbs_str'].append(decnum(input, phrase_index, phrase_length))
    return id.SEM_OK


def semantic_b_string(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['tbs_str'].append(binnum(input, phrase_index, phrase_length))
    return id.SEM_OK


def semantic_x_string(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['tbs_str'].append(hexnum(input, phrase_index, phrase_length))
    return id.SEM_OK


def semantic_trg_op(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_PRE):
        data['min'] = 0
        data['max'] = 0
    else:
        if(data['min'] > data['max']):
            min = str(data['min'])
            max = str(data['max'])
            msg = 'TRG, terminal range, min(' + min + ') > max(' + max + ')'
            data['errors'].append({'line': data['find_line'](phrase_index),
                                   'index': phrase_index, 'msg': msg})
        else:
            data['top_rule']['opcodes'].append({
                'type': id.TRG,
                'min': data['min'],
                'max': data['max'],
            })
    return id.SEM_OK


def semantic_dmin(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['min'] = decnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_dmax(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['max'] = decnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_bmin(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['min'] = binnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_bmax(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['max'] = binnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_xmin(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['min'] = hexnum(input, phrase_index, phrase_length)
    return id.SEM_OK


def semantic_xmax(state, input, phrase_index, phrase_length, data):
    if(state == id.SEM_POST):
        data['max'] = hexnum(input, phrase_index, phrase_length)
    return id.SEM_OK
