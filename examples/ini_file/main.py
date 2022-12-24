''' @file examples/ini_file/main.py
@brief The driver function for the ini file demonstration.
@dir examples/ini_file
@brief This director contains all the file for the ini file example.

This is a demonstration of a substantial, "real life" application
using the Python APG parser generator and the parser
that it generates. A [standard ini file format](https://en.wikipedia.org/wiki/INI_file)
is defined in the file, examples/ini_file/grammar.abnf.
The corresponding grammar object is in the file examples/ini_file/grammar.py
and was generated with Python APG, apg.py, with the command
> python3 %apg.py --input examples/ini_file/grammar.abnf
The sample data parsed by this example is in the file examples/ini_file/data.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
print(os.getcwd())
from apg_py.lib import utilities as utils
from pprint import pprint
from examples.ini_file.ini_file import IniFile

title = '''This is a demonstration of building a substantial
"real life", parser for parsing the well-known ini file format
for key/value pairs in possibly named sections.
This parser recognizes an ini file format similar to the
one described here(https://en.wikipedia.org/wiki/INI_file).
'''
print()
print(title)

ini = IniFile()
print('IniFile.help()')
print(ini.help())

fname = 'examples/ini_file/data'
# fd = open(fname, 'r')
# data = fd.read()
# fd.close()
# print('\nThe ini file.')
# print(data)

ini.parse_ini_file(fname)
print('\n1) display the anonymous key names')
keys = ini.get_keys()
pprint(keys)

print('\n2) for each key display the values')
for key in keys:
    values = ini.get_values(key)
    # print(key, end=' - ')
    print(key + ' -')
    for value in values:
        print(' - ', end='')
        print(value)
    # pprint(values)

print('\n3) display the section names')
sections = ini.get_sections()
pprint(sections)

print('\n3) display the section key names')
for section in sections:
    keys = ini.get_section_keys(section)
    print('[' + section + ']: ', end='')
    pprint(keys)

print('\n4) for each section and key, display the values')
for section in sections:
    keys = ini.get_section_keys(section)
    for key in keys:
        values = ini.get_section_values(section, key)
        print('[' + section + ']:' + key, end=' - ')
        pprint(values)
