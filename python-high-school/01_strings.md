# Strings

## Agenda

- Strings
- Character encoding
- Notable escape sequences
- Formatting numbers
- Bonus track: Formatting
- Bonus track: reserved words

---

## Strings

In python you can define a string using single or double quotes:

```python
# Use the most convenient quotes depending on the string.
a_string = "Ciao, I'm Roberto"
another_string = 'I "love" python'
```

----

A string is a finite, ordered sequence of typographic characters
(e.g., from an alphabet, like the one thaught at school).

Exercise: finite strings using an alphabet $\mathcal{A} : |\mathcal{A}| = k$.

- How many strings of length $n=8$ can you build?
- How many strings of length $m : m \le n=8$, included the empty string, can you build?
- 🦾 Can you generalize the solution for any $n$ and $k$?

Hint: use the following cell to compute the answer.

```python
k = 2
n = 8
solution = 1 + ...  # compute the solution here
print(solution)
```

<!-- sum([2**i for i in range(0, 9)]) -->

---

Here we represent the set of all finite strings with $\mathcal{S}$.

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

While at school we learn the alphabet with 26 letters,
we actually use a much larger alphabet in our daily life:
we use numbers, spaces (e.g. ``, a new line, ), punctuation, emojis, and so on.

To communicate these charactes at the speed of light, we need to
transmit them using electric signals.
The Morse code was the first way of encoding characters
made to be transmitted using electric signals.

Nowadays computers represents typographic characters with numbers,
that are then encoded in sequences of $0$ and $1$ and transmitted using electric signals.

The most common way of mapping characters to numbers is the Extended ASCII table.
Since the basic computer unit is the byte, the Extended ASCII table is limited to 256 characters.

$
byte \in \mathbb{Z}_{255} : = \{ z : z \in \mathbb{Z}; 0 \le z \le 255 \} \\
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
formatting: \mathbb{Q} \rightarrow \mathcal{S}
$

```python
# bin() and hex() returns a string representation
# of an integer number. These are *different* formatting functions.
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

Processing a string to create a number is called parsing (:it: analisi grammaticale).

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
s_a += f"that can be extended"
```

----

```python
# Exercise: print the value of s_a
```

----

```python
# Further formatting is done using ":", eg.
# {:.6} -> limit the string to 6 characters
# {:3.2} -> limit the string to 3 characters, 2 after the decimal point

s_a = f"{s_a} even with {'positional':.6} formatting.\n"
```

----

```python
# Alignment identifiers are simpler: < left , ^ center,  > right
n = 100
s_a = f"Align {n:>10}% python!"
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
