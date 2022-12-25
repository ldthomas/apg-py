# Python APG

[**Introduction**](#id_introduction)<br>
[**GitHub Installation**](#id_installation)<br>
[**PyPi Installation**](#id_pypi)<br>
[**The Pattern-Matching Engine**](#id_apgexp)<br>
[**Documentation**](#id_documentation)<br>
[**License**](#id_license)

### Introduction {#id_introduction}

APG – an ABNF Parser Generator – was originally designed to generate recursive-descent parsers directly from the
[ABNF](https://www.rfc-editor.org/rfc/rfc5234) grammar defining the sentences or phrases to be parsed.
The approach is to recognize that ABNF defines a tree with seven types of nodes and that each node represents
an operation that can guide a depth-first traversal of the tree – that is, a recursive-descent parse of the tree.

However, APG has since evolved from parsing the strictly Context-Free languages described by ABNF in a number of significant ways.

The first is through disambiguation.
A Context-Free language sentence may have more than one parse tree that correctly parses the sentence.
That is, different ways of phrasing the same sentence.
APG disambiguates, attempting each alternative from left to right until a successful parse if found.
All other alternatives are then ignored. A "first success" disambiguation.

From here it was quickly realized that this method of defining a tree of node operations did not in any way
require that the nodes correspond to the ABNF-defined tree.
They could be expanded and enhanced in any way that might be convenient for the problem at hand.
The first expansion was to add the [look ahead](https://en.wikipedia.org/wiki/Syntactic_predicate) nodes.
That is, operations that look ahead for a specific phrase and then continue or not depending on whether the phrase is found.
Next nodes with user-defined operations were introduced.
That is, a node operation that is hand-written by the user for a specific phrase-matching problem.
Finally, to develop an ABNF-based pattern-matching engine similar to
[regular expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp),
a number of new node operations have been added: look behind, back referencing, and begin and end of string anchors.

These additional node operations enhance the original ABNF set but do not change them. Rather they form a superset of ABNF, or as is referred to here, SABNF. If you are new to APG or ABNF a good place to start might be the complete discussion
of the ABNF and superset operators given [here](docs/SABNF.md).

Today, APG is a versatile, well-tested generator of parsers.
And because it is based on ABNF, it is especially well suited to parsing the languages of many Internet technical specifications.
In fact, it is the parser of choice for several large Telecom companies.
Previous versions of APG have been developed to generate parsers in
[C](https://github.com/ldthomas/apg-7.0),
[Java](https://github.com/ldthomas/apg-java)
and [JavaScript](https://github.com/ldthomas/apg-js)(or on [npm](https://www.npmjs.com/package/apg-js)).
Here for the first time is APG in Python.

### GitHub Installations {#id_installation}

You can install Python APG from GitHub by either cloning it or downloading the zip file.
The only difference is the directory name of the installation.
Throughout an Ubuntu-flavored Linux OS is assumed.

<p>**Cloning**</p>
<p>From your project directory execute
> git clone https://github.com/ldthomas/apg-py.git<br>
> cd apg-py
</p>
<p>**Zip File**</p>
<p>Download the zip file from [https://github.com/ldthomas/apg-py](https://github.com/ldthomas/apg-py).
From your project directory execute
> unzip apg-py-main.zip<br>
> cd apg-py-main
</p>
<p>
**Testing**
</p>
<p>
The directory `apg_py` has a stand-alone grammar object generator,
`generator.py`.
To make a quick test that all is in order execute the generator help screen.
> python3 %apg_py --help
You should see the generator help screen.
</p>
<p>
Further tests are in the `tests` directory. Run
> python3 -m unittest discover
which should indicate something like 138 successful tests.
</p>
<p>
There is also a large set of examples demonstrating most aspects 
of using Python APG in the `examples` directory.
Each sub-directory in the examples directory has a file `main.py`.
Use it to execute the examples in that classification. 
For example,
> python3 %examples/basics/main.py --help
will list a number of examples of the most basic usage of Python APG.
Examine, debug or tweak any of the other files in the folder to
familiarize yourself with how Python APG can be put to work in your
own projects.
</p>
<p>
See this [quick start](docs/quick_github.md) guide for building an APG parser in your project
using the GitHub installation.
</p>

### PyPi Installations {#id_pypi}

The simplest way to install Python APG is simply

> pip install apg-py

This will install the `%apg_py` library and CLI stand-alone grammar object generator,
but none of the tests or examples that are available from the GitHub installation.

<p>
See this [quick start](docs/quick_pip.md) guide for building and APG parser in
your project with the `pip` installation.
</p>

### The Pattern-Matching Engine {#id_apgexp}

The class [**ApgExp**](classapg__py_1_1exp_1_1exp_1_1ApgExp.html) is a regex-like pattern-matching engine which uses SABNF as the pattern-defining syntax
and APG as the pattern-matching parser.
While regex has a long and storied history and is heavily integrated into modern programming languages and practice,
ApgExp offers the full pattern-matching power of APG and the reader-friendly SABNF syntax.
It is fully recursive, meaning nested parenthesis matching, and introduces a new recursive mode of back referencing,
enabling, for example, the matching of name tags in nested start and end HTML tags.

Though not specifically designed and built to address the regex issues discussed
[here by Larry Wall](https://raku.org/archive/doc/design/apo/A05.html),
creator of the Perl language, ApgExp does seem to go a long way toward addressing many of those issues.
Most notably back referencing and nested patterns, but other issues as well.

First introduced in JavaScript APG [[1](https://github.com/ldthomas/apg-js)]
[[2](https://www.npmjs.com/package/apg-js)] as an alternative to
[RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) in 2017,
this extends it to the Python language.

### Documentation {#id_documentation}

<p>
This documentation is in triple string comments in the code. To generate the documentation
install [Graphviz](https://graphviz.org/) and [doxygen](https://www.doxygen.nl/index.html).
> sudo apt update<br>
> sudo apt install graphviz<br>
> sudo apt install doxygen<br>
> unzip apg-py-main.zip<br>
> cd apg-py-main<br>
> doxygen
The documentation home page will be `html/index.html`.
Or view it on the [APG website](https://sabnf.com/docs/python/index.html)
</p>

### License {#id_license}

2-Clause BSD License.

<pre>
Copyright &copy; 2022 Lowell D. Thomas, all rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>
