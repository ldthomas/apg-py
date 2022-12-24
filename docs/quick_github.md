## A Quick Start Parser from the GitHub Installation

### The Project Structure

<p>
    Throughout this example we will assume the project structure:
<pre>
|my_project_folder
|---|apg-py-main.zip
    |my_project
    |---__init__.py
    |---dynamic.py
    |---grammar.abnf
    |---static.py
</pre>
All commands will be executed from the <code>my_project_folder</code> directory.
The content of the files will be presented and explained as we go.
</p>

### Installation

<p>
    Make sure the PyPI version of <code>apg-py</code> is not installed.
    Otherwise it will override the local GitHub version.
<pre>
> pip uninstall apg-py
</pre>
</p>
<p>
    Install the GitHub version of <code>apg-py</code> and make sure it is working.
<code>
<pre>
> unzip apg-py-main.zip
> cp -r apg-py-main/apg_py .
> python3 apg_py --version
</pre>
</code>
</p>

### A Dynamic Generator with Parsing

<p>
The <code>dynamic.py</code> file should look like this.<br>
<code>
<pre>
import sys
import os
sys.path.append(os.getcwd()) # required to find apg_py
from apg_py.lib import utilities as util
from apg_py.lib.parser import Parser
from apg_py.api.api import Api
abnf = 'S = "a" S / "y"\\n'
input = 'aaay'
api = Api()
grammar = api.generate(abnf)
if(api.errors):
    print('\n1) Grammar Errors')
    print(api.display_errors())
    exit()
parser = Parser(grammar)
result = parser.parse(utils.string_to_tuple(input))
print('\n1) Parser Result')
print(result)
</pre>
</code>
</p>
<p>
    Execute the command:
<code>
<pre>
> python3 my_project/dynamic.py
</pre>
</code>
You should see the results of a successful parse.
<pre>
1) Parser Result
            success: True
              state: 101
              STATE: MATCH
       input_length: 4
          sub_begin: 0
            sub_end: 4
         sub_length: 4
      phrase_length: 4
  max_phrase_length: 4
          node_hits: 17
     max_tree_depth: 13
</pre>
</p>

### A Parsing from a Pre-Generated Grammar

<p>
    Let's now do the same project except that we will generate the grammar
    object using the stand-alone generator.
The ABNF grammar syntax file, <code>grammar.abnf</code>, is simply,
<code>
<pre>
S = "a" S / "y"
</pre>
</code>
(Make sure the line ends with a line feed.)
</p>
<p>
    To convert this
    to the grammar object file <code>%grammar.py</code>:
<code>
<pre>
> python3 apg_py --input my_project/grammar.abnf
</pre>
</code>
You should see the output
<pre>
grammar object written to file my_project/grammar.py
</pre>
</p>
<p>
    The <code>static.py</code> file should look like,<br>
<code>
 <pre>
import sys
import os
sys.path.append(os.getcwd()) # required to find apg_py
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
import grammar
print('The ABNF Syntax')
print(%grammar.to_string())
input = 'aaay'
parser = Parser(grammar)
result = parser.parse(utils.string_to_tuple(input))
print('\n1) Parser Result')
print(result)
</pre>
</code>
</p>
<p>
    Now execute the static parser with,
<code>
<pre>
> python3 my_project/static.py
</pre>
</code>
    The output should look like,

<pre>
The ABNF Syntax
S = "a" S / "y"

1. Parser Result
    success: True
    state: 101
    STATE: MATCH
    input_length: 4
    sub_begin: 0
    sub_end: 4
    sub_length: 4
    phrase_length: 4
    max_phrase_length: 4
    node_hits: 17
    max_tree_depth: 13
 </pre>
  </p>
