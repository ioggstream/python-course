## Mathematical built-int functions

Python has some built-in functions for numbers:

```python
M = max(1, 2)
m = min(1, 2, -3)
absolute_value = abs(-3)
approximate_positive = round(1.4)
approximate_negative = round(-1.4)
```

Execise:

- see the [python manual](https://docs.python.org/3/library/functions.html)
for a list of built-in functions;
- share with your classmates the ones you know.

Mathematical built-in functions can be used to implement simple algorithms,
such as the Euclidean algorithm for the greatest common divisor (GCD)
(:it: massimo comun divisore - MCD)

```python
# Let's define two positive integers.
b = 234
c = 64
# Reorder the numbers so that b is smaller than c.
b, c = min(b, c), max(b, c)
print("b =", b, "c =", c)
```

Now execute the cell below many times, and see what happens.

```python
# Iterate until b is zero.
d = c - b
b, c = min(d, b), max(d, b)
print("b =", b, "c =", c)
```

---

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
