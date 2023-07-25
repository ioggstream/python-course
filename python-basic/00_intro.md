# Python for System Administrator

 Author: <roberto.polli@par-tec.it>

---

## Introducing Python

Python is an interpreted, object oriented language with
a lot of built in features.

This is a fast-track course for sysadmin with knowledge
of languages like Perl, PHP, C and Java

----

## Agenda

- Importing features
- Getting help
- Printing
- Basic Arithmetic
- Variable assignment
- Formatting

----

```python
# Importing_new_features
# ..is easy. Features are collected
# in packages or modules. Just
import telnetlib  # to use a
telnetlib.Telnet  # client
```

```python
# We can even import single classes
#  from a module, like
from telnetlib import Telnet

```

----

Modules contain documentation in the form of docstrings,
that jupyter presents in scrollable boxes.

```python

# Read the module documentation...
help(telnetlib)
```

```python
# ...or the class documentation
help(Telnet)

```

---

## Basic functions

There are basic functions for printing and
managing variables.

```python
# you can print with the print() function
print("Hello world!")
```

```python
# concatenate string with a + sign
# and using hex notation
print("Hello" + " " + "World\x21")
```

```python
print("Ciao")
```

```python
# prefixing a string with 'r' disables the
# interpretation of the string content
print('Hello' * 2 + r'World\x21')
```

----

```python
# the chr() function returns the corresponding
# character of an integer. While \n and \t are
# just the usual notation for linefeed and tab
print(chr(72) + "ello\n\tWorld!")
```

```python
# triple-quoting allows multi-line strings
# %s works like in the C printf() function
# but operates on strings
# ord() is just the inverse of chr()
print("""The answer is

%s
""" % ord('*'))

```

---

## Basic Arithmetic

```python
# This is a comment, while
a = 1  # is an integer variable
b = 0x10  # is another integer in hex notation
```

----

```python
# Exercise: use the print() function to print the value of a and b.

```

----

```python
# c = 011  # ...another one in C-style oct on python 2...
c = 0o11  # ...in python 2 and 3
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

---

## Variable assignment

```python
# variable_assignment
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
# but if right-side values are not defined, I get an exception
e, f = c, e + d
```

----

```python
# The function ord() returns the integer value of a character.
ord('*')
```

```python
# The function chr() returns the character corresponding to an integer.
ord("\n")
```

---

#### Bonus topic: reserved words

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

---

## Formatting numbers

```python
# bin() and hex() returns a string representation
# of a number
a, b1 = hex(10), bin(1)
```

```python
# Exercise: which is the type of a? And the type of b1?
type(a)
```

----

```python
# while the format() function can be more flexible
#  10 = 8ciphers + 2chars for the '0b' header
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

---

## Formatting

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

```python

```

----
