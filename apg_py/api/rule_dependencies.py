''' @file apg_py/api/rule_dependencies.py
@brief Determine which rules each rule depends on and vice versa.'''
from apg_py.lib import identifiers as id
from pprint import pprint


def rule_dependencies(rules, udts, rule_names, udt_names):
    '''Determine the rule dependencies and
    recursive types for each rule.
    @param rules The rules from the syntax & semantic phases.
    @param udts The UDTs from the syntax & semantic phases.
    @param rule_names The NameList object (see class Api)for looking up
    rule name indexes.
    @param udt_names The NameList object for
        looking up UDT name indexes.
    @returns The rule dependencies object.
    '''

    rule_range = range(len(rules))

    def scan(index, is_scanned):
        rdi = rule_deps[index]
        is_scanned[index] = True
        for op in rules[index]['opcodes']:
            if(op['type'] == id.RNM):
                rdop = rule_deps[op['index']]
                rdi['refers_to'][op['index']] = True
                if(is_scanned[op['index']] is False):
                    scan(op['index'], is_scanned)
                for j in rule_range:
                    if(rdop['refers_to'][j]):
                        rdi['refers_to'][j] = True
                for j in range(udt_count):
                    if(rdop['refers_to_udt'][j]):
                        rdi['refers_to_udt'][j] = True
            elif(op['type'] == id.UDT):
                rdi['refers_to_udt'][op['index']] = True
            elif(op['type'] == id.BKR):
                lookup = rule_names.get(op['lower'])
                if(lookup == -1):
                    lookup = udt_names.get(op['lower'])
                    if(lookup == -1):
                        raise Exception(
                            'back referenced name is not a rule or UDT')
                    rdi['refers_to_udt'][lookup['index']] = True
                else:
                    rdi['refers_to'][lookup['index']] = True

    # initialize all rule dependencies
    rule_count = len(rules)
    udt_count = len(udts)
    rule_deps = []
    for i in rule_range:
        rule_deps.append({
            'refers_to': [False] * rule_count,
            'is_referenced_by': [False] * rule_count,
            'refers_to_udt': [False] * udt_count,
            'recursive_type': id.ATTR_N,
            'group_no': -1
        })

    # discover which rules each rule refers to
    for i in rule_range:
        is_scanned = [False] * rule_count
        scan(i, is_scanned)

    # discover all rules which each rule is referenced by
    for i in rule_range:
        for j in rule_range:
            if(rule_deps[j]['refers_to'][i]):
                rule_deps[i]['is_referenced_by'][j] = True

    # find the recursive rules
    for i in rule_range:
        if(rule_deps[i]['refers_to'][i]):
            rule_deps[i]['recursive_type'] = id.ATTR_R

    # find the mutually-recursive groups, if any
    group_count = -1
    for i in rule_range:
        rdi = rule_deps[i]
        if(rdi['recursive_type'] == id.ATTR_R):
            new_group = True
            for j in rule_range:
                if(j != i):
                    rdj = rule_deps[j]
                    if(rdj['recursive_type'] == id.ATTR_R):
                        if(rdi['refers_to'][j] and rdj['refers_to'][i]):
                            if(new_group):
                                group_count += 1
                                new_group = False
                                rdi['recursive_type'] = id.ATTR_MR
                                rdi['group_no'] = group_count
                            rdj['recursive_type'] = id.ATTR_MR
                            rdj['group_no'] = group_count
    return rule_deps


def display_deps(rule_deps, rules, udts, alpha=True):
    '''Display the rule dependencies.
    @param rule_deps The rule dependencies.
    The returned object from the @ref rule_dependencies() function.
    @param rules The rules from the syntax & semantic phases.
    @param udts The UDTs from the syntax & semantic phases.
    @param alpha If True (default), rules are listed alphabetically.
    Otherwise, they are listed in the order in which they appear
    in the grammar syntax.
    @returns The display string.
    '''
    RULES_LINE = 8

    def alpha_rules(val):
        return rules[val]['lower']

    def alpha_udts(val):
        return udts[val]['lower']

    def type(val):
        return rule_deps[val]['recursive_type']

    def group(val):
        return rule_deps[val]['group_no']

    rule_count = len(rules)
    udt_count = len(udts)
    rule_range = range(rule_count)
    udt_range = range(udt_count)
    rule_alphas = [0] * rule_count
    udt_alphas = [0] * udt_count
    for i in rule_range:
        rule_alphas[i] = rules[i]['index']
    for i in range(udt_count):
        udt_alphas[i] = udts[i]['index']
    if(alpha):
        rule_alphas.sort(key=alpha_rules)
        udt_alphas.sort(key=alpha_udts)
    show = ''
    # compute max name length
    length = 0
    for i in rule_range:
        rlen = len(rules[i]['name'])
        if(rlen > length):
            length = rlen
    fmt = '%' + str(length) + 's: '
    show += (fmt + 'legend\n') % ('')
    show += (fmt + '=> (rule refers to)\n') % ('rule')
    show += (fmt + '<= (rule is referenced by)\n\n') % ('rule')
    for ii in rule_range:
        i = rule_alphas[ii]
        # show += (fmt + '%s\n') % (rules[i]['name'],
        #                           id.dict.get(rule_deps[i]['recursive_type']))
        counti = 0
        show += (fmt + '=> ') % (rules[i]['name'])
        for kk in rule_range:
            if(rule_deps[i]['refers_to'][kk]):
                counti += 1
        for kk in udt_range:
            if(rule_deps[i]['refers_to_udt'][kk]):
                counti += 1
        if(counti):
            count = 0
            for jj in rule_range:
                j = rule_alphas[jj]
                k = rule_deps[i]['refers_to'][j]
                if(k):
                    if(count % RULES_LINE == 0 and count > 1):
                        show += ('\n' + fmt + '=> ') % ('')
                    show += rules[j]['name']
                    if(count < counti - 1):
                        show += ', '
                    count += 1
            for jj in udt_range:
                j = udt_alphas[jj]
                k = rule_deps[i]['refers_to_udt'][j]
                if(k):
                    if(count % RULES_LINE == 0 and count > 1):
                        show += ('\n' + fmt + '=> ') % ('')
                    show += udts[j]['name']
                    if(count < counti - 1):
                        show += ', '
                    count += 1
        show += '\n'
        show += (fmt + '<= ') % ('')
        counti = 0
        for kk in rule_range:
            if(rule_deps[i]['is_referenced_by'][kk]):
                counti += 1
        if(counti):
            count = 0
            for jj in rule_range:
                j = rule_alphas[jj]
                k = rule_deps[i]['is_referenced_by'][j]
                if(k):
                    if(count % RULES_LINE == 0 and count > 1):
                        show += ('\n' + fmt + '<= ') % ('')
                    show += rules[j]['name']
                    if(count < counti - 1):
                        show += ', '
                    count += 1
        show += '\n'
    return show
