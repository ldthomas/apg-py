''' @file apg_py.py
@brief This is the APG command line parser grammar generator.
It takes an input SABNF grammar syntax and generates a
grammar object suitable for use with a Python APG parser.
<pre>
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the input SABNF source file name (see note 1)
  -o OUTPUT, --output OUTPUT
                        the output grammar file name (see note 2)
  -v, --version         display the version and copyright information
  -s, --strict          allow only strict ABNF (RFC5234 & RFC7405) syntax
  --dry-run             inhibits output file generation
  -dr, --display-rules  display the grammar rule and UDT(if any) names
  -dd, --display-rule-dependencies
                        for each rule, display the rules it references and all rules referring to it
  -da, --display-rule-attributes
                        for each rule, display the rule attributes (left-recursive, etc.)
  --index               if specified, rules are displayed by index(the order they appear in the grammar), otherwise alphabetically

NOTES: 1) Multiple input files can be specified with by comma-separated names. The files will be concatenated in the order in which they appear. 2) The output file name is
optional. If no output name is specified the first input name will be stripped of its extension, if any, and the extension ".py" added.
</pre>
'''
import os
import sys
import argparse
sys.path.append(os.getcwd())
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
from apg_py.api.api import Api


def get_source(file_names):
    '''Get the list of input file names, open them and concatenate the files.
    Construct the default output file name from the first input name.'''
    # get the list of file names
    names = file_names.split(',')
    name_range = range(len(names))
    for i in name_range:
        names[i] = names[i].replace(' ', '')
    source = ''
    for name in names:
        fd = open(name, 'r')
        source += fd.read()
        fd.close()

    # strip extension, if any, from first file name
    dir_name = os.path.dirname(names[0])
    base_name = os.path.basename(names[0])
    exts = base_name.split('.')
    len_exts = len(exts)
    if(len_exts > 1):
        if(len(exts) == 2):
            base_name = exts[0]
        else:
            base_name = exts[0]
            for i in range(1, len_exts - 1):
                base_name += '.' + exts[i]
    default_output = dir_name + os.path.sep + base_name + '.py'
    return {'source': source, 'default_output': default_output}


desc = '''
This is Python APG - an ABNF Parser Generator.
It generates a grammar object from a superset of ABNF(SABNF)
suitable for use with the APG parser.
'''
ep = '''NOTES: 1) Multiple input files can be specified with by
comma-separated names.
The files will be concatenated in the order in which they appear.
2) The output file name is optional. If no output name is specified
the first input name will be stripped of its extension, if any,
and the extension ".py" added.
'''


def main():
    parser = argparse.ArgumentParser(
        prog='apg-py',
        description=desc,
        epilog=ep
    )
    parser.add_argument(
        '-i',
        '--input',
        help='the input SABNF source file name (see note 1)',
        dest='input',
        required=False,
        action='store')
    parser.add_argument('-o', '--output',
                        help='the output grammar file name (see note 2)',
                        dest='output',
                        action='store')
    parser.add_argument('-v', '--version',
                        help='display the version and copyright information',
                        dest='version',
                        action='store_true')
    parser.add_argument('-s', '--strict',
                        help='allow only strict ABNF (RFC5234 & RFC7405) syntax',
                        dest='strict',
                        action='store_true')
    parser.add_argument('--dry-run',
                        help='inhibits output file generation',
                        dest='dry_run',
                        action='store_true')
    parser.add_argument(
        '-dr',
        '--display-rules',
        help='display the grammar rule and UDT(if any) names',
        dest='display_rules',
        action='store_true')
    hlp = 'for each rule, display the rules it references '
    hlp += 'and all rules referring to it'
    parser.add_argument(
        '-dd',
        '--display-rule-dependencies',
        help=hlp,
        dest='display_dependencies',
        action='store_true')
    parser.add_argument(
        '-da',
        '--display-rule-attributes',
        help='for each rule, display the rule attributes (left-recursive, etc.)',
        dest='display_attributes',
        action='store_true')
    hlp = 'if specified, rules are displayed by index'
    hlp += '(the order they appear in the grammar), '
    hlp += 'otherwise alphabetically'
    parser.add_argument(
        '--index',
        help=hlp,
        dest='index',
        action='store_true')
    args = parser.parse_args()

    if(args.version):
        # handle the version request
        text = 'Python APG version 1.0'
        text += '\nCopyright (c) 2022 Lowell D. Thomas'
        print(text)
        exit()

    if(not args.input):
        # input SABNF file name required
        print('--input argument required.', end=' ')
        print('Use --help for options and descriptions.')
        exit()

    # get the SABNF source
    result = get_source(args.input)

    # generate the grammar object
    api = Api()
    api.generate(result['source'], args.strict)
    if(api.errors):
        print('\nGRAMMAR ERRORS')
        print(api.display_errors())
        print()
        print('ANNOTATED GRAMMAR')
        print(api.display_grammar())
        exit()

    if(args.display_rules):
        sort_type = 'alpha'
        if(args.index):
            sort_type = 'index'
        print('\nGRAMMAR RULES')
        print(api.display_rules(sort_type))

    if(args.display_dependencies):
        sort_type = 'alpha'
        if(args.index):
            sort_type = 'index'
        print('\nRULE DEPENDENCIES')
        print(api.display_rule_dependencies(sort_type))

    if(args.display_attributes):
        sort_type = 'alpha'
        if(args.index):
            sort_type = 'index'
        print('\nRULE ATTRIBUTES')
        print(api.display_rule_attributes(sort_type))

    if(not args.dry_run):
        outname = args.output if(args.output) else result['default_output']
        api.write_grammar(outname)
        print('grammar object written to file ' + outname)
