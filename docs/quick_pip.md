## A Quick Start Parser from the pip Installation

### The Project Structure

<p>
    Throughout this example we will assume the project structure:
<pre>
|my_project_folder
|---|my_project
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
    Make sure <code>apg-py</code> is installed and working.
<code>
<pre>
> pip install apg-py
> apg-py --version
</pre>
</code>

(Note that the stand-alone generator, `apg-py`, comes as a CLI application with the pip installation.)

</p>

### A Dynamic Generator with Parsing

In this example, the ABNF grammar and the generation of the grammar object
will be done dynamically within the parser program.
The <code>dynamic.py</code> file should look like this.
<code>

<pre>
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
    object in advance and import it into the parser.
The ABNF syntax is now in the file <code>grammar.abnf</code>:
<code>
<pre>
S = "a" S / "y"
</pre>
</code>
(Make sure the line ends with a line feed.)
</p>
<p>
    Now execute the command:

<code>
<pre>
> apg-py --input my_project/grammar.abnf
</pre>
</code>

You should see the output:

<code>
<pre>
grammar object written to file my_project/grammar.py
</pre>
</code>
</p>
<p>
    The <code>static.py</code> file should look like,<br>
 
 <code>
 <pre>
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
    Now execute the static parser with,<br>
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
