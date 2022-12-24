''' @file apg_py/api/rule_attributes.py
@brief Compute the rule attributes for all rules.
'''
from apg_py.lib import identifiers as id


# from unicodedata import name


class Attr():
    '''Simple class for attribute data for each rule.'''

    def __init__(self, name='dummy', type=id.ATTR_N, group=-1):
        '''Attr constructor.
        @param name The name of the rule this attribute applies to.
        @param type The identifier of the rule's recursive type.
        @param group The group number if the type is
        mutually-recursive (ATTR_MR),
        otherwise, -1.
        '''
        self.left = False
        self.nested = False
        self.right = False
        self.empty = False
        self.finite = False
        self.cyclic = False
        self.leaf = False
        self.is_open = False
        self.is_complete = False
        self.name = name
        self.lower = name.lower()
        self.type = type
        self.group = group

    def reset(self):
        '''Reset all attributes to false.'''
        self.left = False
        self.nested = False
        self.right = False
        self.empty = False
        self.finite = False
        self.cyclic = False
        self.leaf = False
        self.is_open = False
        self.is_complete = False

    def dup(self):
        '''Create a duplicate attribute object from the present one.
        @returns Returns new attribute object identical to the present one.
        '''
        cpy = Attr()
        cpy.left = self.left
        cpy.nested = self.nested
        cpy.right = self.right
        cpy.empty = self.empty
        cpy.finite = self.finite
        cpy.cyclic = self.cyclic
        cpy.leaf = self.leaf
        cpy.is_open = self.is_open
        cpy.is_complete = self.is_complete
        cpy.name = self.name
        cpy.lower = self.lower
        cpy.type = self.type
        cpy.group = self.group
        return cpy

    def copy(self, cpy):
        '''Copy a given attribute into the present attribute.
        @param cpy The attribute to copy.
        '''
        self.left = cpy.left
        self.nested = cpy.nested
        self.right = cpy.right
        self.empty = cpy.empty
        self.finite = cpy.finite
        self.cyclic = cpy.cyclic
        self.leaf = cpy.leaf
        self.is_open = cpy.is_open
        self.is_complete = cpy.is_complete
        self.name = cpy.name
        self.lower = cpy.lower
        self.type = cpy.type
        self.group = cpy.group


def rule_attributes(rules, rule_deps):
    '''Compute the recursive and non-recursive attributes for each rule.
    @param rules The list of rules.
    @param rule_deps The rule dependencies previously computed
    (see @ref rule_dependencies.py)
    @returns Returns the rule attributes and any errors as a dictionary
    {'errors': errors, 'attributes': attrs}
    '''
    # internal functions
    def op_eval(opcodes, op_index):
        func = switch.get(opcodes[op_index]['type'])
        if(func is None):
            raise Exception(
                'op_eval: unrecognized opcode type',
                opcodes[op_index]['type'])
        return func(opcodes, op_index)

    def op_alt(opcodes, op_index):
        # generate a list of child attributes
        op = opcodes[op_index]
        op_range = range(len(op['children']))
        child_attrs = []
        for i in op_range:
            child_attrs.append(Attr())

        # compute each child attribute
        for i in op_range:
            child_attrs[i] = op_eval(opcodes, op['children'][i])

        # if any child attribute is true ALT is true
        attr_op = Attr()
        for attr in child_attrs:
            if(attr.left):
                attr_op.left = True
            if(attr.nested):
                attr_op.nested = True
            if(attr.right):
                attr_op.right = True
            if(attr.cyclic):
                attr_op.cyclic = True
            if(attr.empty):
                attr_op.empty = True
            if(attr.finite):
                attr_op.finite = True
        return attr_op

    def is_recursive(attr):
        if(attr.left or attr.nested or attr.right or attr.cyclic):
            return True
        return False

    def is_cat_nested(attrs):
        children = len(attrs)
        # 1) if any child is nested, CAT is nested
        for attr in attrs:
            if(attr.nested):
                return True

        # 2) if the left-most right-recursive child is
        #    followed by at least one non-empty, non-right-recursive child
        for i in range(children):
            attri = attrs[i]
            if(attri.right and not attri.leaf):
                for j in range(i + 1, children):
                    attrj = attrs[j]
                    if(not attrj.empty and not attrj.right
                       and not attrj.cyclic):
                        return True

        # 3) if the right-most left-recursive child is preceded
        #    by at least one non-empty non-left-recursive child
        for i in range(children - 1, -1, -1):
            attri = attrs[i]
            if(attri.right and not attri.leaf):
                for j in range(i - 1, -1, -1):
                    attrj = attrs[j]
                    if(not attrj.empty and not attrj.left
                       and not attrj.cyclic):
                        return True

        # 4) if there is at least one recursive child between the
        #    left-most and right-most non-recursive non-empty children
        for i in range(children):
            attri = attrs[i]
            if(not attr.empty and not is_recursive(attri)):
                for j in range(i + 1, children):
                    if(is_recursive(attrs[j])):
                        for k in range(j + 1, children):
                            attrk = attrs[k]
                            if(not attrk.empty
                               and not is_recursive(attrk)):
                                return True

        # none of the above
        return False

    def is_cat_cyclic(attrs):
        # if all children are cyclic, CAT is cyclic
        for attr in attrs:
            if(not attr.cyclic):
                return False
        return True

    def is_cat_left(attrs):
        # if the left-most non-empty child is left, CAT is left
        for attr in attrs:
            if(attr.left):
                return True
            if(not attr.empty):
                return False
            # keep looking
        return False

    def is_cat_right(attrs):
        # if the right-most non-empty child is right, CAT is right
        for i in range(len(attrs) - 1, -1, -1):
            if(attrs[i].right):
                return True
            if(not attrs[i].empty):
                return False
            # keep looking
        return False

    def is_cat_empty(attrs):
        # if all children are empty, CAT is empty
        for attr in attrs:
            if(not attr.empty):
                return False
        return True

    def is_cat_finite(attrs):
        # if all children are finite, CAT is finite
        for attr in attrs:
            if(not attr.finite):
                return False
        return True

    def op_cat(opcodes, op_index):
        # generate a list of child attributes
        op = opcodes[op_index]
        op_range = range(len(op['children']))
        child_attrs = []
        for i in op_range:
            child_attrs.append(Attr())

        # compute each child attribute
        for i in op_range:
            child_attrs[i] = op_eval(opcodes, op['children'][i])

        # compute CAT attributes from child attributes
        attr_op = Attr()
        attr_op.left = is_cat_left(child_attrs)
        attr_op.nested = is_cat_nested(child_attrs)
        attr_op.right = is_cat_right(child_attrs)
        attr_op.cyclic = is_cat_cyclic(child_attrs)
        attr_op.empty = is_cat_empty(child_attrs)
        attr_op.finite = is_cat_finite(child_attrs)
        return attr_op

    def op_rep(opcodes, op_index):
        attr_op = op_eval(opcodes, op_index + 1)
        if(opcodes[op_index]['min'] == 0):
            attr_op.empty = True
            attr_op.finite = True
        return attr_op

    def op_rnm(opcodes, op_index):
        index = opcodes[op_index]['index']
        rule_eval(index)
        return working_attrs[index].dup()

    def op_bkr(opcodes, op_index):
        attr_op = Attr()
        bkr_op = opcodes[op_index]
        if(bkr_op['is_udt']):
            attr_op.empty = bkr_op['empty']
            attr_op.finite = True
        else:
            # use the empty and finite values for the rule
            index = bkr_op['index']
            rule_eval(index)
            attr_op.copy(working_attrs[index])

            # however, this is a terminal node like TBS
            attr_op.left = False
            attr_op.nested = False
            attr_op.right = False
            attr_op.cyclic = False
        return attr_op

    def op_and(opcodes, op_index):
        attr_op = op_eval(opcodes, op_index + 1)
        attr_op.empty = True
        return attr_op

    def op_tls(opcodes, op_index):
        attr_op = Attr()
        attr_op.empty = len(opcodes[op_index]['string']) == 0
        attr_op.finite = True
        attr_op.cyclic = False
        return attr_op

    def op_tbs(opcodes, op_index):
        attr_op = Attr()
        attr_op.empty = False
        attr_op.finite = True
        attr_op.cyclic = False
        return attr_op

    def op_udt(opcodes, op_index):
        attr_op = Attr()
        attr_op.empty = opcodes[op_index]['empty']
        attr_op.finite = True
        attr_op.cyclic = False
        return attr_op

    def op_anchor(opcodes, op_index):
        attr_op = Attr()
        attr_op.empty = True
        attr_op.finite = True
        attr_op.cyclic = False
        return attr_op
    switch = {
        id.ALT: op_alt,
        id.CAT: op_cat,
        id.REP: op_rep,
        id.RNM: op_rnm,
        id.BKR: op_bkr,
        id.AND: op_and,
        id.NOT: op_and,
        id.BKA: op_and,
        id.BKN: op_and,
        id.TLS: op_tls,
        id.TBS: op_tbs,
        id.TRG: op_tbs,
        id.UDT: op_udt,
        id.ABG: op_anchor,
        id.AEN: op_anchor}

    def rule_eval(rule_index):
        attri = working_attrs[rule_index]
        if(attri.is_complete):
            return
        if(not attri.is_open):
            # open the rule an traverse it
            attri.is_open = True
            attr_op = op_eval(rules[rule_index]['opcodes'], 0)
            attri.left = attr_op.left
            attri.nested = attr_op.nested
            attri.right = attr_op.right
            attri.cyclic = attr_op.cyclic
            attri.finite = attr_op.finite
            attri.empty = attr_op.empty
            attri.leaf = False
            attri.is_open = False
            attri.is_complete = True
            return
        # recursive leaf
        if(rule_index == start_rule):
            attri.left = True
            attri.right = True
            attri.cyclic = True
            attri.leaf = True
            return

        # terminal leaf
        attri.finite = True

    # end internal functions

    # compute the attributes
    # initialize the attributes
    rule_count = len(rules)
    rule_range = range(rule_count)
    attrs = []
    working_attrs = []
    for i in rule_range:
        attrs.append(
            Attr(
                rules[i]['name'],
                rule_deps[i]['recursive_type'],
                rule_deps[i]['group_no']))
        working_attrs.append(
            Attr(
                rules[i]['name'],
                rule_deps[i]['recursive_type'],
                rule_deps[i]['group_no']))

    # compute the rule attributes
    for i in rule_range:
        for attr in working_attrs:
            attr.reset()
        start_rule = i
        rule_eval(i)
        attrs[i].copy(working_attrs[i])

    # check for errors
    errors = []
    for i in rule_range:
        attr = attrs[i]
        rule = rules[i]
        if(attr.cyclic):
            errors.append({'line': rule['line'],
                           'index': 0,
                           'msg': 'rule ' + rule['name'] + ' is cyclic'})
        if(attr.left):
            errors.append({'line': rule['line'],
                           'index': 0,
                           'msg': 'rule ' + rule['name'] +
                           ' is left recrusive'})
        if(not attr.finite):
            errors.append(
                {
                    'line': rule['line'],
                    'index': 0,
                    'msg': 'rule ' + rule['name'] +
                    ' only matches infinte strings'})

    # return the attributes
    return {'errors': errors, 'attributes': attrs}


def display_rule_attributes(attrs_arg, mode='index'):
    '''Display all rule attributes.
    @param attrs_arg The attributes to display.
    @param mode The display mode
        - 'index' Display attributes of rules in the order
        they appear in the grammar syntax.
        - 'type' Display attributes grouped by recursive type,
        listed alphabetically within each type.
        - 'alpha' Display attributes alphabetically by rule name.
    @returns Returns a string of the display.
    '''
    def sort_alpha(val):
        return val.lower

    def sort_type(val):
        return val.type

    def sort_group(val):
        return val.group

    attrs = []
    for attr in attrs_arg:
        attrs.append(attr.dup())
    if(mode == 'type'):
        attrs.sort(key=sort_alpha)
        attrs.sort(key=sort_type)
        attrs.sort(key=sort_group)
    elif(mode == 'alpha'):
        attrs.sort(key=sort_alpha)
    # default is to display by rule index
    fmt = '%6s: %6s: %6s: %6s: %6s: %6s: %6s: %6s: %s\n'
    display = ''
    display += (fmt % ('left', 'nested',
                'right', 'cyclic', 'finite',
                       'empty', 'type',
                       'group',
                       'rule name'))

    def yes_or_no(val):
        if(val):
            return 'yes'
        return 'no'

    def display_type(val):
        if(val == id.ATTR_N):
            return 'N'
        if(val == id.ATTR_R):
            return 'R'
        if(val == id.ATTR_MR):
            return 'MR'
        return '??'
    for attr in attrs:
        left = yes_or_no(attr.left)
        nested = yes_or_no(attr.nested)
        right = yes_or_no(attr.right)
        cyclic = yes_or_no(attr.cyclic)
        finite = yes_or_no(attr.finite)
        empty = yes_or_no(attr.empty)
        type = display_type(attr.type)
        if(attr.type == id.ATTR_N or attr.type == id.ATTR_R):
            group = '--'
        else:
            group = str(attr.group)
        if(attr.type == id.ATTR_MR):
            group = str(attr.group)
        display += (fmt % (left, nested, right, cyclic,
                    finite, empty, type, group, attr.name))

    return display
