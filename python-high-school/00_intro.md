# Python for System Administrator

 Author: <roberto.polli@par-tec.it>

---

## Introducing Python

Python is an interpreted, object oriented language with
a lot of built in features.
It can be used as a calculator and for  mathematical operations,
such as statistics, plotting and linear algebra.

This is a fast-track course for high school students with math knowledge.

Students are expected to type and execute cells, and share their results.

---

# Jupyter

Is the course environment in your browser.
It requires a modern browser and an internet connection supporting
websockets. If your network setup (e.g. your proxy)
does not support websockets, you will not be able to
execute the code.

---

While you might find the exercises' solutions in the environment,
it is important for you to spend some time trying to do your homework!
This will help you to remember the concepts and to learn how to use the tools.

---

## What can I do with Jupyter?

You can:

- execute the next cell with `SHIFT+ENTER` (try it now!)

If your environment supports it, you can use features requiring
operating system access:

- [open a (named) terminal on the local machine](/terminals/example)
- [edit an existing file](/edit/notebooks/untitled.txt)

---

- add more cells with `ALT+ENTER`

----

Try to add a cell below this one and write some text in it.

```python
# Add a new python cell with ALT+ENTER.
```

---

## Python terminal

With Jupyter, you have a Python terminal at your disposal.
You can run Python code:

```python
# You can evaluate maths and strings
s = 1
print("a string and the number " + str(s))
```

Jupyter remembers the variables you define in a cell, so you can use them in the next cells.

```python
# Evaluate this cell with SHIFT+ENTER
s = s + 1
print("now s is increased " + str(s))
```

Since Jupyter remembers the variables, you can run the cells in any order you want.
This means that sometimes, you need to "reset" the environment, to start from scratch.

This can be done with the "Kernel > Restart" or "Kernel > Restart & Clear output" menu.

----

## Agenda

- Printing
- Basic Arithmetic
- Variable assignment
- Formatting
- Importing modules
- Getting help

---

## Basic functions

There are basic functions for printing and
managing variables.

```python
# you can print with the print() function
print("Hello world!")
```

```python
# concatenate strings with a + sign
# and using hex notation
print("Hello" + " " + "World!")
```

```python
print("Ciao")
```

---

## Basic Arithmetic

A python variable is a label that can be associated to a value.

```python
# This is a comment, while
a = 1       # is an integer
b = 16.0    # a float
c = 1.2e2   # another float in exponential notation
```

----

```python
# Exercise: use the print() function to print the value of a, b and c.

```
----

```python
# I can sum, multiply, and modulus
print(a + b, 5 % 2)
```

----

```python
# Exercise: which is the expected value of 2 * c?
print(2 * c)
```

----

### Representing numbers

A number is represented using digits (in Italian, "cifre"):

- the decimal notation uses 10 digits, from 0 to 9;
- the binary notation uses 2 digits, 0 and 1;
- the octal notation uses 8 digits, from 0 to 7;
- the hexadecimal notation uses 16 digits, where 10 is represented by A, 11 by B, and so on.

A number in base $b$ is represented as:

$$
\sum_{i=0}^{n} c_i b^i = c_0 b^0 + c_1 b^1 + c_2 b^2 + \dots + c_n b^n
$$

where $c_i$ is the $i$-th digit of the number.

Python supports the binary, the octal and the hexadecimal notation too!

```python
d = 0b11  # integer in binary notation
e = 0o11  # integer in octal notation
f = 0x10  # integer in hexadecimal (hex) notation
g = 0x1F  # integer in hex notation
```

Exercise:

```python
# Use this cell to print the values of d, e, f and g.
```

Questions:

- What is a bit?
- What is a byte?
- Why in the computer world the hex notation is very common?

---

## Variable assignment

```python
# I can assign more than one variable on the same line
a, b, c = 1, 2, 3
d, string_a, string_b = a + b, "foo", "bar"
```

```python

# ...swap them...
(a, b) = (b, a)
```

```python
# Exercise: print the values of the above variables
```

```python
# but if right-side values are not defined, I get an error (aka exception)
e, f = c, e + d
```

---

## Strings

A string is a finite, ordered sequence of typographic characters (e.g., from an alphabet).

Exercise: finite strings using an alphabet $\mathcal{A}$ where $|\mathcal{A}| = k$.

- How many strings of length $n=8$ can you build?
- How many strings of length $m \le n, n=8$, included the empty string, can you build?
- 🦾 Can you generalize the solution for any $n$ and $k$?

Hint: use the following cell to compute the answer.

```python
k = 2
n = 8
solution = 1 + ...  # compute the solution here
print(solution)
```

We can represent the set of all finite strings with $\mathcal{S}$.

In python you can define a string using single or double quotes:

```python
a_string = "Ciao"
another_string = "2πr"
```

Python defines some operations on strings:

```python
print("a" + "b")  # concatenation
print("a" * 3)    # repetition
```

You can template strings using the f-string notation:

```python
a = 1
print(f"the value of a is {a}")
```

Exercise:

```python
# Use this cell to print the value of a_string and another_string
```

---

### Character encoding

Computers represents typographic characters with numbers.
The most common is the Extended ASCII table, that maps numbers to characters.

Since the basic computer unit is the byte, the Extended ASCII table is limited to 256 characters.

$
byte \in \mathbb{Z}_{255} := \mathbb{Z} \cap [0, 255] \\
\mathcal{A} = \{ a, b, c, \dots, A, B, C, \dots, ", !, ?, \dots  \}
$

$
chr : \mathbb{Z}_{255} \rightarrow \mathcal{A} \\
ord : \mathcal{A} \rightarrow \mathbb{Z}_{255}
$

```python
# The function chr() returns the character corresponding to an integer.
chr(42)
```

```python
# The function ord() returns the integer value of a character.
ord('*')
```

Nowadays, the most common character encoding is UTF, that is a superset of ASCII.
It uses more than one byte to represent a character,
so it can represent up to $17 * 2^{16}$ characters
from different languages and symbols like emojis.

```python
smile = '😀'
print(smile, "->", ord(smile))
```

```python
# prefixing a string with 'r' disables the
# interpretation of the string content
print('Hello' * 2 + r'World\x21')
```

----

### Notable escape sequences

You can print special characters such as
`new line` or `tabular spaces` using the escape sequence notation.

```python
# The \n and \t are
# just the usual notation for newline and tab
print("Hello\n\tWorld!")
```

```python
# triple-quoting allows multi-line strings
answer = ord('*')
print(f"""The answer is

{answer}
""")

```

---

## Formatting numbers

Formatting means representing a number with a string.
Note: it is impossible to represent all the real numbers with finite strings ;)

$
formatting: \mathbb{Z} \rightarrow \mathcal{S}
$

```python
# bin() and hex() returns a string representation
# of a number. These are *different* formatting functions.
a, b1 = hex(10), bin(1)
```

```python
# Exercise: which is the type of a? And the type of b1?
type(a)
```

----

```python
# The format() function is very flexible
#  10 = 8digits + 2chars for the '0b' header
binary_with_leading_zeroes = format(1, '#010b')
```

----

```python
# and reversible with
b1 == int(binary_with_leading_zeroes, base=2)
```

----

```python
# Exercise: use this cell to inspect the values of the above variables.
```

```python
# Exercise: use this cell to compute the value of the hexadecimal number `abc`.
# Hint: read the int function manual.
help(int)
```
---

## Bonus track: Formatting

----

```python
# The new str.format function just replaces
#  %s and %d with {}.
s_a = "is a string "

print(s_a)
```

----

```python
# A string
s_a += "that can {} extended".format("be")
```

----

```python
# Exercise: print the value of s_a
```

----

```python
# Further formatting is done using ":", eg.
#  %.6s -> {:.6}
#  %3.2d -> {:3.2}
s_a = "{} even with {:.6} formatting.\n".format(s_a, "positional")
```

----

```python
# Alignment identifiers are simpler: < left , ^ center,  > right
s_a = "Align {:>10}% python!".format(100)
print(s_a)
print("just prints a string")
```

----

```python
# Exercise: modify s_a to align the string to the left and to the center.
```

---

### Formatting with names

----

```python
# You can name variables to get
# a better formatting experience ;)
fmt_a = "{name:<.3} {nick:^.8} {sn:>30}"
print(fmt_a.format(name="-"*10, nick="*"*15, sn="-"*40))
print(fmt_a.format(name="Roberto", nick="ioggstream", sn="Polli"))
```

----

## Importing functionalities

----

```python
# Importing new features
# ..is easy. Features are collected
# in packages or modules. Just
import math  # to use the
math.sqrt  # function

math.sqrt(2)
```

```python
# We can even import single functions
#  or constants from a module
from math import pi as π
π / 2
```

----

Modules contain documentation in the form of docstrings,
that jupyter presents in scrollable boxes.

```python

# Read the module documentation...
help(math)
```

```python
# ...or the function documentation
help(math.sqrt)

```

---

#### Bonus track: reserved words

Python has a set of reserved words that cannot be used as variable names, including:

- `if, else, for, while, and, or, not, in, is, break, continue, pass, def, class, return, try, except, finally, lambda`.

Sadly, some core, built-in function names in python 2 can be used as variable names, including:

- `file, print, len, type, list, exit`.

This means that a programmer can accidentally overwrite the built-in function with a variable of the same name, causing unexpected results.

Now we will see an example of this, and how to fix it using the built-in module.

```python
# We should respect reserved words and built-in functions, like print, ord...
print(("ord:\x20", ord))

```

----

```python
# We can discover the original module of an object with
print(ord.__module__)
```

----

Note:

- python 2 uses the `__builtin__` module, while
- python 3 uses the `builtins` module.

In both cases, you should never use the `__builtins__` module (note the final **s**), because it's implementation dependent.
For further information on this topic, see [the python execution model documentation](https://docs.python.org/3/reference/executionmodel.html#builtins-and-restricted-execution)

----

```python
# If we override a function and call it...
ord = 4
ord('*')  # ...ooops!
```

```python
# We can fix it up importing the version specific built-in module
#   and reassigning the variable to the original function

try:  # Try the python 2 syntax...
    import __builtin__ as builtins
except ImportError:  # And if it fails, use the python 3 syntax.
    import builtins

ord = builtins.ord
ord('*')  # ...ooops!
```
