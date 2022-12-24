''' @file apg_py/api/semantic.py
@brief Semantic translation of the SABNF AST.

The AST is computed in the syntax phase (@ref syntax.py).
The AST is translated to generate all rules, UDTs and opcodes.
'''
from apg_py.lib import identifiers as id


def semantic(api):
    '''Translate the AST, generating a list of rule objects,
    and UDT objects, if any.
    @param api The api object for the grammar syntax (@ref api.py)'''
    data = {}
    data['find_line'] = api.find_line
    data['rules'] = []
    data['udts'] = []
    data['errors'] = []
    data['rule_names'] = api.NameList()
    data['udt_names'] = api.NameList()
    api.ast.translate(data)
    rules = data['rules']
    remove_redundant_opcodes(rules)
    return {
        'errors': data['errors'],
        'rules': rules,
        'udts': data['udts'],
        'rule_names': data['rule_names'],
        'udt_names': data['udt_names']}


def remove_redundant_opcodes(rules):
    '''Opcodes ALT and CAT with only one child are redundant
    and can be removed.
    Opcodes REP with min = max = 1 are redundant and can be removed.
    @param rules The grammar object rules.'''
    for rule in rules:
        i = 0
        opcodes = rule['opcodes']
        while(i < len(opcodes)):
            i = check_for_removal(i, opcodes)
            if(i < len(opcodes)):
                del(opcodes[i])


def check_for_removal(i, opcodes):
    '''Scan all opcodes and check for ALT, CAT and REP that can be removed.
    @param i The opcode index of reference.
    @param opcodes The list of opcodes for a given rule.
    @returns Returns the number of remaining opcodes after removal.'''
    for j in range(i, len(opcodes)):
        opj = opcodes[j]
        if(opj['type'] == id.ALT or opj['type'] == id.CAT):
            if(len(opj['children']) == 1):
                # remove this ALT, adjust other children indexes
                adjust_children(j, opcodes)
                return j
        elif(opj['type'] == id.REP and opj['min'] == 1 and opj['max'] == 1):
            adjust_children(j, opcodes)
            return j
    return len(opcodes)


def adjust_children(j, opcodes):
    '''When an opcode is removed the indecies of the ALT and CAT children
    must be corrected for the removed opcodes.
    @param j The opcode index of reference.
    @param opcodes The list of opcodes for a particular rule.'''
    for op in opcodes:
        if(op['type'] == id.ALT or op['type'] == id.CAT):
            if(len(op['children'])):
                for m in range(len(op['children'])):
                    if(op['children'][m] > j):
                        op['children'][m] -= 1
