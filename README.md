# Python APG

<p>
APG – an ABNF Parser Generator – generates parsers directly from a superset of 
<a href="https://www.rfc-editor.org/rfc/rfc5234"><b>ABNF</b></a>.
A detailed description of ABNF and the superset (SABNF) is given 
<a href="https://github.com/ldthomas/apg-py/blob/main/docs/SABNF.md"><b>here</b></a>
</p>

### Installation

<p>
Python APG can be installed from either 
<a href="https://github.com/ldthomas/apg-py"><b>GitHub</b></a>
or
<a href="https://pypi.org/project/apg-py/"><b>PyPI</b></a>.
The PyPI installation will provide the generator and parsing library.
However, the GitHub installation additionally provides an extensive
set of examples, a large set of tests and the full documentation.
</p>

### Quick Start Guides

<p>
A quick start parser guide using the GitHub installation can be found 
<a href="https://github.com/ldthomas/apg-py/blob/main/docs/quick_github.md"><b>here</b></a>.
</p>

<p>
A quick start parser guide using the PyPI installation can be found 
<a href="https://github.com/ldthomas/apg-py/blob/main/docs/quick_pip.md"><b>here</b></a>.
</p>

### Documentation

<p>
The full documentation is in the code and in additional documentation files.
It can be generated
with <a href="https://www.doxygen.nl/"><b>doxygen</b></a>
from the GitHub installation. For example, using the GitHub zip download
and the Linux command line:
<code>
<pre>
unzip apg-py-main.zip
cd apg-py-main
sudo apt install graphviz
sudo apt install doxygen
doxygen
</pre>
</code>
The documentation home page will now be found in <code>html/index.html</code>.
Or you can view it directly from the 
<a href="https://sabnf.com/docs/python/index.html"><b>APG website</b></a>.
</p>
