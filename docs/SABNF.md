# Superset Augmented Backus-Naur Form (SABNF)

-   <a href="#id_overview"><b>Overview</b></a>
-   <a href="#id_abnf"><b>ABNF</b></a>
    -   <a href="#id_rules">rules</a>
    -   <a href="#id_terminals">terminals</a>
    -   <a href="#id_nonterminals">non-terminals</a>
    -   <a href="#id_groups">groups</a>
    -   <a href="#id_optional">optional groups</a>
    -   <a href="#id_comments">comments</a>
    -   <a href="#id_example">example</a>
-   <a href="#id_restrictions"><b>Restrictions</b></a>
-   <a href="#id_sabnf"><b>Superset Operators</b></a>
    -   <a href="#id_udts">user-defined terminals</a>
    -   <a href="#id_lookahead">look ahead</a>
    -   <a href="#id_lookbehind">look behind</a>
    -   <a href="#id_backreferences">back references</a>
    -   <a href="#id_anchors">anchors</a>
-   <a href="#id_summary"><b>Operator Summary</b></a>
-   <a href="#id_grammar"><b>ABNF for SABNF</b></a>

<h3>Overview</h3>
<a id="id_overview"></a>

<p>
Augmented Backus-Naur Form (ABNF) is a popular formal syntax for describing Internet specifications.
It is officially described in the Internet standards publications of the
[IETF](https://www.ietf.org/), RFC 5234 and RFC 7405. A detailed explanation of ABNF is given here.
However, if there any discrepancies between what is given here and the RFCs, the RFCs naturally prevail.
</p>
<p>
Additionally, in the development [**APG**](https://sabnf.com)(an 
<strong>A</strong>BNF <strong>P</strong>arser <strong>G</strong>enerator),
 its parsers and pattern-matching engines,
it has been found convenient to enhance ABNF's features. Since the enhancement features add to 
ABNF without altering any of its existing features, it is referred to here
as a Superset of ABNF or SABNF.
</p>

<h3>ABNF</h3>
<a id="id_abnf"></a>

ABNF is a syntax to describe phrases, a phrase being any string of positive integers.
Because the integers so often represent the [ASCII](http://www.asciitable.com/) character codes there are special
ABNF features to accommodate an easy description of ASCII strings. Consequently, phrase integers
are often referred to here as character codes. However, the meaning and range of the
ABNF phrase integers are entirely up to the user.
The complete ABNF syntax description of a phrase
is called a grammar and the terms "grammar" and "ABNF syntax" will be used synonymously here.

<h4>Rules</h4>
<a id="id_rules"></a>

Phrases are described with named rules. A rule name is alphanumeric with hyphens allowed after the first character.
Rule names are case insensitive. A rule definition has the form:

```
name = elements CRLF
```

where the equal sign, `=`, separates the name from the phrase definition.
Elements are made up of terminals, operators and other rule names, as described below.
Each rule must end with a carriage return, line feed combination, CRLF.
Each line must begin in the first column (see [restrictions](#id_restrictions) below).
A rule definition may be continued with continuation lines, each of which begins with a space or tab.

<h4>Terminals</h4>
<a id="id_terminals"></a>

Rules resolve into a string of terminal phrase integers. ABNF provides several means of representing terminal
integers and strings of integers or character codes explicitly.

_single characters_

```
%d32     - represents the decimal integer character code 32
%x20     - represents the hexidecimal integer character code 20 or decimal 32
%b100000 - represents the binary integer character code 100000 or decimal 32
```

_strings of characters_

```
%d13.10     - represents the line ending character string CRLF
%x0D.0A     - represents the line ending character string CRLF
%b1101.1010 - represents the line ending character string CRLF
```

_range of characters_

```
%d48-57         - represents any single character code in the decimal range 48 through 57
                  that is, any ASCII digit 0, 1, 2, 3 ,4, 5, 6, 7, 8 or 9
%x30-39         - represents any single character code in the hexidecimal range 30 through 39
                  (also any ASCII digit)
%b110000-111001 - represents any single character code in the binary range 110000 through 111001
                  (also any ASCII digit)
```

_literal strings of characters_<br>

```
"ab"   - represents the case-insensitive string "ab" and would match
         %d97.98, %d65.98, %d97.66 or %d65.66 ("ab", "Ab", "aB" or "AB")
%i"ab" - defined in RFC 7405, is a case-insensitive literal string (identical to "ab")
%s"ab" - defined in RFC 7405, is a case-sensitive literal string (identical to %d97.98)
```

Tab characters, `0x09`, are not allowed in literal strings.

_prose values_  
When all else fails, ABNF provides a means for the grammar's author to simply provide a prose explanation of the phrase in the form of a spoken, as opposed to formal, language. The notation is informative and the parser generator will recognize it as valid ABNF. However, since there are no formal specifics, the generator will halt without generating a parser.

```
<phrase description in prose>
```

Tab characters, `0x09`, are not allowed in prose values.

<h4>Non-Terminals</h4>
<a id="id_nonterminals"></a>

_concatenation_  
One or more spaces and/or tabs between elements in a rule definition represents a concatenation of the two elements.
For example, consider the two rules,

```
AB1 = "a" "b" CRLF
AB2 = "ab" CRLF
```

The space between the two elements `"a"` and `"b"` acts as a concatenation operator.
The effect in this case is that rule `AB1` defines the same phrase as rule `AB2`.

_alternatives_  
The forward slash, `/`, is the alternative operator. The rule

```
AB = "a" / "b" CRLF
```

would match either the phrase `a` or the phrase `b`.

_incremental alternatives_  
While not a new operation, incremental alternatives are a sometimes-convenient means of adding alternatives to a rule.

```
alt1 = "a" / "b" / "c" CRLF
alt2 = "a" CRLF
      / "b" CRLF
      / "c" CRLF
alt3 = "a" / "b" CRLF
alt3 =/ "c" CRLF
```

Rules `alt1`, `alt2` and `alt3` have identical definitions. The incremental alternative, `=/`, allows for adding additional alternatives to a rule at a later date. As seen in `alt2`, the same affect can be achieved with line continuations. However, in some cases, it may be convenient or even essential to add additional alternatives later in the grammar. For example, if the grammar is broken into two or more files. In such a case, line continuations would not be possible and the incremental alternative becomes an essential syntactic addition.

Note that the rule name of an incremental alternative statement must have been previously defined in a rule definition
or an error will occur.

_repetitions_  
An element modifier of the general form `n*m (0 <= n <= m)` can be used to indicate a repetition of the element
a minimum of `n` times and a maximum of `m` times. For example, the grammar

```
number = 2*3digit CRLF
digit  = %d48-57  CRLF
```

would define a phrase that could be any number with 2 or 3 ASCII digits.
There are a number of shorthand variations of the repetition operator.

```
*  = 0*infinity (zero or more repetitions)
1* = 1*infinity (one or more repetitions)
*1 = 0*1 (zero or one repetitions, optional)
2  = 2*2 (exactly two repetitions)
```

<h4>Groups</h4>
<a id="id_groups"></a>

Elements may be grouped with enclosing parentheses. Grouped elements are then treated as a single element
within the full context of the defining rule. Consider,

```
phrase1 = elem (foo / bar) blat CRLF
phrase2 = elem foo / bar blat CRLF
phrase3 = (elem foo) / (bar blat) CRLF
```

`phrase1` matches `elem foo blat` or `elem bar blat`, whereas `phrase2` matches `elem foo` or `bar blat`.
A word of caution here. Concatenation has presidence over (tighter binding than) alternation so that `phrase2`
is the same as `phrase3` and not `phrase1`.
It can be confusing. Use parentheses liberally to keep the grammar meaning clear.

Another useful way to think of groups is as anonymous rules. That is, given

```
phrase1 = elem (foo / bar) blat CRLF
phrase2 = elem anon blat CRLF
anon    = foo /bar CRLF
```

phrase1 and phrase2 are identical. Only phrase2 utilizes the explicit rule `anon` for the parenthesized grouping. In phrase1, the parenthesized grouping anonymously defines the same rule as `anon`.

<h4>Optional Groups</h4>
<a id="id_optional"></a>

Elements grouped with square brackets, `[]`, are optional groups. Consider,

```
phrase1 = [elem foo] bar blat CRLF
phrase2 = 0*1(elem foo) bar blat CRLF
```

Both phrases are identical and will match either `elem foo bar blat` or `bar blat`.

<h4>Comments</h4>
<a id="id_comments"></a>

Comments begin with a semicolon, `;`, and continue to the end of the current line.
For example, in the following rule definition, everything from the semicolon to CRLF is considered white space.

```
phrase = "abc"; any comment can go here   CRLF
```

In this implementation empty lines and comment-only lines are accepted as white space,
but any line beginning with one or more space/tab characters and having text not beginning
with a semicolon will be rejected as an ABNF syntax error.
Consider the lines,

```
1:CRLF
2:    CRLF
3:;comment CRLF
4:     ; comment CRLF
5:   comment CRLF
```

Lines `1:` through `4:` are valid blank lines. Line `5:` would be regarded as a syntax error.

<h4>Bringing it all together now</h4>
<a id="id_example"></a>

Here is an example of a complete ABNF grammar representing the general definition of a floating point number.

```
float    = [sign] decimal [exponent]
sign     = "+" / "-"
decimal  = integer [dot [fraction]]
           / dot fraction
integer  = 1*%d48-57
dot      = "."
fraction = 1*%d48-57
exponent = "e" [esign] exp
esign    = "+" / "-"
exp      = 1*%d48-57
```

<h3>Restrictions</h3>
<a id="id_restrictions"></a>

This **APG** implementation imposes a several restrictions and changes to the strict ABNF described above. These are minor changes except for the disambiguation rules.

**Indentations**  
RFC 5234 specifies that a rule may begin in any column, so long as all rules begin in the same column. This implementation restricts the rules to the first column.

**Line Endings**  
RFC 5234 specifies that a line ending must be the carriage return/line feed pair, CRLF. This implementation relaxes that and accepts CRLF, LF or CR as a valid line ending. However, the last line must have a line ending or a fatal error is generated. (_Forgetting a line ending on the last line is a common and annoying error, but keeping the line ending requirement has been a conscious design decision._)

**Case-Sensitive Strings**  
This implementation allows case-sensitive strings to be defined with single quotes.

```
phrase1 = 'abc'      CRLF
phrase2 = %s"abc"    CRLF
phrase3 = %d97.98.99 CRLF
```

All three of the above phrases defined the identical, case-sensitive string `abc`. The single-quote notation for this was introduced in 2011 prior to publication of RFC 7405. The SABNF single-quote notation is kept for backward compatibility.

**Empty Strings**  
Some rules may accept empty strings. That is, they match a string with 0 characters. To represent an empty string explicitly, two possibilities exist.

```
empty-string = 0*0element ; zero repetitions
empty-string = ""         ; empty literal string
```

In this implementation only the literal string is allowed. Zero repetitions will halt the parser generator with a grammar error.

**Disambiguation**  
The ALT operation allows the parser to follow multiple pathways through the parse tree. It can be and often is the case that more than one of these pathways will lead to a successful phrase match. The question of what to do with multiple matches was answered early in the development of **APG** with the simple rule of always trying the alternatives left to right as they appear in the grammar and then simply accepting the first to succeed,
ignoring any remaining alternatives, if any. This "first success" disambiguation rule may break the context-free aspect of ABNF, but it not only solves the problem of what to do with multiple matches, at least on a personally subjective level, it actually makes the grammars easier to write. That is, easier to arrange the alternatives to achieve the desired phrase definitions.

Related to disambiguation is the question of how many repetitions to accept. Consider the grammar

```
reps = *"a" "a" CRLF
```

A strictly context-free parser should accept any string a<sup>n</sup>, n>0. But in general this requires some trial and error with back tracking. Instead, repetitions in **APG** always accept the longest match possible. That would mean that **APG** would fail to match the example above. However, a quick look shows that a simple rewrite would fix the problem.

```
reps = 1*"a" CRLF
```

Longest-match repetitions rarely lead to a serious problem. Again, knowing in advance exactly how the parser will handle repetitions allows for easy writing of a correct grammar.

<h2>Superset ABNF (SABNF)</h2>
<a id="id_sabnf"></a>

In addition to the seven original node operations defined by ABNF, **APG** recognizes an addition eight operations. Since these do not alter the original seven operations in any way, taken together they constitute a super set of the original set.
Hence the designation SABNF(<strong>S</strong>uperset <strong>A</strong>ugmented <strong>B</strong>ackus-<strong>N</strong>aur <strong>F</strong>orm).

The user-defined terminals and look ahead operations have been carried over from previous versions of **APG**. Look behind, anchors and back references have been developed to replicate the phrase-matching power of various flavors of
[`regex`](https://en.wikipedia.org/wiki/Regular_expression).
However, the recursive mode of [back referencing](#id_backreferences) is, to my knowledge,
a new **APG** development with no previous counterpart in other parsers or phrase-matching engines.

<h4>User-Defined Terminals</h4>
<a id="id_udts"></a>

In addition to the ABNF terminals above, **APG** allows for User-Defined Terminals (UDT).
These allow the user to write any phrase he or she chooses as a code snippet. The syntax is,

```
phrase1 = u_non-empty CRLF
phrase2 = e_possibly-empty CRLF
```

UDTs begin with `u_` or `e_`. The underscore is not used in the ABNF syntax, so the syntax parser can easily
distinguish between UDT names and rule names. The difference between the two forms is that a UDT
beginning with `u_` may not return an empty phrase. If it does the parser will raise an exception.
Only if the UDT name begins with `e_` is an empty phrase return accepted. The difference has to do with
fatal rule attributes such as left recursion and will not be discussed here further.

Note that even though UDTs are terminal phrases, they are also named phrases and share
many named-phrase qualities with rules.

<h4>Look Ahead</h4>
<a id="id_lookahead"></a>

The look ahead operators are modifiers like repetitions. They are left of and adjacent to the phrase
that they modify.

```
phrase1 = &"+" number CRLF
phrase2 = !"+" number CRLF
number  = ["+" / "-"] 1*%d48-75 CRLF
```

`phrase1` uses the positive look ahead operator. If `number` begins with a `"+"` then `&"+"` returns the
empty phrase and parsing continues. Otherwise, `&"+"` returns failure and `phrase1` fails to find a match.
That is, `phrase1` accepts only numbers that begin with `+`, e.g.`+123`.

`phrase2` uses the negative look ahead operator. It works just as described above except that it succeeds if
`"+"` is _not_ found and fails if it is.
That is, `phrase2` accepts only numbers that begin with no sign or with a negative sign. e.g. `-123` or `123`

A good discussion of the origin of these operators can be found in this
[Wikipedia article.](https://en.wikipedia.org/wiki/Syntactic_predicate)

<h4>Look Behind</h4>
<a id="id_lookbehind"></a>

The look behind operators are modifiers very similar to the look ahead operators, the difference, as the name implies, is that they operate on phrases behind the current string index instead of ahead of it.

```
phrase1 = any-text &&line-end text CRLF
phrase2 = any-text !!line-end text CRLF
text = *%d32-126 CRLF
any-text = *(%d13.10 / %d10 / %d13 / %d32-126) CRLF
line-end = %d13.10 / %d10 / %d13 CRLF
```

`phrase1` will succeed only if `text` is preceded by a `line-end`.
`phrase2` will succeed only if `text` is _not_ preceded by a `line-end`.

Look behind was introduced specifically for the **APG** phrase-matching engine.
It may have limited use outside of this application.

<h4>Back References</h4>
<a id="id_backreferences"></a>

Back references are terminal strings similar to terminal literal and binary strings. The difference being that terminal literal and strings are predefined in the grammar syntax and back reference strings are defined with a previous
rule name or UDT match.

```
phrase1 = A \A CRLF
phrase2 = A \%iA CRLF
phrase3 = A \%sA CRLF
phrase4 = u_myudt \u_myudt
A       = "abc" / "xyz" CRLF
```

The back reference, `\A` will attempt a case-insensitive match to whatever phrase was matched by A.
(The notation works equally for rule names and UDT names.)
Therefore, `phrase1` would match `abcabc` or `abcABC`, etc., but not `abcxyz`. The `%i` and `%s` notation
is used to indicate case-insensitive and case-sensitive matches, just as specified in RFC 7405
for literal strings. Therefore, `phrase3` would match `xYzxYz` but not `xYzxyz`.

These back reference operations were introduced specifically to match the parsing power of
various flavors of `regex` pattern-matching engines.
However, it was soon recognized that another mode of back referencing was possible.
The particular problem to solve was, how to use back referencing to match tag names
in the nested opening and closing tags of HTML and XML.
This led to the development of a new type of back referencing, which to my knowledge, is unique to **APG**.

I'll refer to the original definition of back referencing above as "universal mode".
The name "universal" being chosen to indicate that the back reference `\%%uA` matches
the last previously occurring phrase `A` universally.
That is, regardless of where in the input source string or parse tree it occurs.

I'll refer to the new type of back referencing as "recursive mode".
The name "recursive" being chosen to indicate that `\%%rA`
matches the last occurrence of `A` on a recursive sub-tree of the parse tree
with the same recursive parent node.
A more detailed explanation with diagrams is given elsewhere.

Case insensitive and universal mode are the defaults unless otherwise specified.
The complete set of back references with modifiers is:

```
\A     = \%iA   = \%uA = \%i%uA = \%u%iA
\%sA   = \%s%uA = \%u%sA
\%rA   = \%i%rA = \%r%iA
\%s%rA = \%r%sA
```

<h4>Anchors</h4>
<a id="id_anchors"></a>

Again, to replicate the pattern matching power of `regex`,
SABNF includes two specific anchors, the beginning and ending of a string.

```
phrase1 = %^ text     CRLF
phrase2 = text %$     CRLF
phrase3 = %^ "abc" %$ CRLF
text    = *%d32-126   CRLF
```

Anchors match a location, not a phrase. `%^` returns an empty string match if the input string character index
is zero and fails otherwise. Likewise, `%$` returns an empty string match if the input string character index
equals the string length and fails otherwise. The leading `%` is taken from the RFC 7405 syntax for modifying
literal strings, and the `^` and `$` characters have been chosen to be similar to their familiar `regex` counterparts.

In the examples above, `phrase1` will match `text` only if it starts at the beginning of the string.
`phrase2` will match `text` only if it ends at the end of a string. `phrase3` will match `abc`
only if it is the entire string. This may seem self evident in this context, but **APG** parsers
allow parsing of sub-strings of the full input string. Therefore, when parsing sub-strings it may not always be known
programmatically whether a phrase is at the beginning or end of a string.

<h3>Operator Summary</h3>
<a id="id_summary"></a>

<table>
<caption><strong>Terminal SABNF operators.</strong></caption>
<tr>
<th>operator</th>
<th>notation</th>
<th>form</th>
<th>description</th>
</tr>
<tr>
<td>TLS</td>
<td>"string"</td>
<td>ABNF</td>
<td>terminal literal string</td>
</tr>
<tr>
<td>TBS</td>
<td>%d65.66.67</td>
<td>ABNF</td>
<td>terminal binary string</td>
</tr>
<tr>
<td>TRG</td>
<td>%d48-57</td>
<td>ABNF</td>
<td>terminal range</td>
</tr>
<tr>
<td>UDT</td>
<td>u_name or<br>e_name</td>
<td>SABNF</td>
<td>User-Defined Terminal</td>
</tr>
<tr>
<td>BKR</td>
<td>\\name or<br>\\u_name</td>
<td>SABNF</td>
<td>back reference</td>
</tr>
<tr>
<td>ABG</td>
<td>%$</td>
<td>SABNF</td>
<td>begin of string anchor</td>
</tr>
<tr>
<td>AEN</td>
<td>%^</td>
<td>SABNF</td>
<td>end of string anchor</td>
</tr>
</table>

<table>
<caption><strong>Non-Terminal SABNF operators.</strong></caption>
<tr>
<th>operator</th>
<th>notation</th>
<th>form</th>
<th>description</th>
</tr>
<tr>
<td>ALT</td>
<td>/</td>
<td>ABNF</td>
<td>alternation</td>
</tr>
<tr>
<td>CAT</td>
<td>white space</td>
<td>ABNF</td>
<td>concatenation</td>
</tr>
<tr>
<td>REP</td>
<td>n*m</td>
<td>ABNF</td>
<td>repetition</td>
</tr>
<tr>
<td>RNM</td>
<td>name</td>
<td>ABNF</td>
<td>rule name</td>
</tr>
<tr>
<td>AND</td>
<td>&</td>
<td>SABNF</td>
<td>positive look ahead</td>
</tr>
<tr>
<td>NOT</td>
<td>!</td>
<td>SABNF</td>
<td>negative look ahead</td>
</tr>
<tr>
<td>BKA</td>
<td>&&</td>
<td>SABNF</td>
<td>positive look behind</td>
</tr>
<tr>
<td>BKN</td>
<td>!!</td>
<td>SABNF</td>
<td>negative look behind</td>
</tr>
</table>

<h3>ABNF for SABNF</h3>
<a id="id_grammar"></a>

RFC 5234 defines the ABNF syntax for the ABNF syntax. While this may seem paradoxical, it makes sense when you realize that a parser generator is a parser whose semantic phase generates a parser.
In the case of **APG**, both the parser of the generator and the parsers it generates are defined with an SABNF syntax.
Here is the ABNF syntax (no superset features required) used by **APG** to generate SABNF parsers.

```
file                = *(blank-line / rule)
blank-line          = *(%d32/%d9) [comment] line-end
rule                = rule-lookup owsp alternation owsp line-end
rule-lookup         = (rule-name) owsp equals
equals              = inc-alt / defined
rule-name           = alphanum
defined             = %d61
inc-alt             = %d61.47
alternation         = concatenation *(owsp alt-op concatenation)
concatenation       = repetition *(cat-op repetition)
repetition          = [modifier] (group / option / element)
modifier            = (predicate [rep-op])
                    / rep-op
predicate           = bka-op
                    / bkn-op
                    / and-op
                    / not-op
element             = udt-op
                    / rnm-op
                    / trg-op
                    / tbs-op
                    / tls-op
                    / cls-op
                    / bkr-op
                    / abg-op
                    / aen-op
                    / pros-val
group               = %d40 owsp  alternation group-close
group-close         = owsp %d41
option              = option-open owsp alternation option-close
option-open         = %d91
option-close        = owsp %d93
rnm-op              = alphanum
bkr-op              = %d92 [bkrModifier] bkr-name
bkrModifier         = (cs [um / rm]) / (ci [um / rm]) / (um [cs /ci]) / (rm [cs / ci])
cs                  = '%s'
ci                  = '%i'
um                  = '%u'
rm                  = '%r'
bkr-name            = uname / ename / rname
rname               = alphanum
uname               = %d117.95 alphanum
ename               = %d101.95 alphanum
udt-op              = udt-empty
                    / udt-non-empty
udt-non-empty       = %d117.95 alphanum
udt-empty           = %d101.95 alphanum
rep-op              = (rep-min star-op rep-max)
                    / (rep-min star-op)
                    / (star-op rep-max)
                    / star-op
                    / rep-min-max
alt-op              = %d47 owsp
cat-op              = wsp
star-op             = %d42
and-op              = %d38
not-op              = %d33
bka-op              = %d38.38
bkn-op              = %d33.33
abg-op              = %d37.94
aen-op              = %d37.36
trg-op              = %d37 ((dec dmin %d45 dmax)
                    / (hex xmin %d45 xmax)
                    / (bin bmin %d45 bmax))
tbs-op              = %d37 ((dec d-string *(%d46 d-string))
                    / (hex x-string *(%d46 x-string))
                    / (bin b-string *(%d46 b-string)))
tls-op              = tls-case %d34 tls-string tls-close
tls-case            = [ci / cs]
tls-close           = %d34
tls-string          = *(%d32-33/%d35-126/string-tab)
string-tab          = %d9
cls-op              = %d39 cls-string cls-close
cls-close           = %d39
cls-string          = *(%d32-38/%d40-126/string-tab)
pros-val            = pros-val-open pros-val-string pros-val-close
pros-val-open       = %d60
pros-val-string     = *(%d32-61/%d63-126/string-tab)
pros-val-close      = %d62
rep-min             = rep-num
rep-min-max         = rep-num
rep-max             = rep-num
rep-num             = 1*(%d48-57)
d-string            = dnum
x-string            = xnum
b-string            = bnum
dec                 = (%d68/%d100)
hex                 = (%d88/%d120)
bin                 = (%d66/%d98)
dmin                = dnum
dmax                = dnum
bmin                = bnum
bmax                = bnum
xmin                = xnum
xmax                = xnum
dnum                = 1*(%d48-57)
bnum                = 1*%d48-49
xnum                = 1*(%d48-57 / %d65-70 / %d97-102)
;
; Basics
alphanum            = (%d97-122/%d65-90) *(%d97-122/%d65-90/%d48-57/%d45)
owsp                = *space
wsp                 = 1*space
space               = %d32
                    / %d9
                    / comment
                    / line-continue
comment             = %d59 *(%d32-126 / %d9)
line-end            = %d13.10
                    / %d10
                    / %d13
line-continue       = (%d13.10 / %d10 / %d13) (%d32 / %d9)
```
