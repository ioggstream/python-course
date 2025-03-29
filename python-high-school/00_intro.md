# Python for High School

 Author: <roberto.polli@par-tec.it>

---

## Introducing Python

Python is an interpreted, object oriented language with
a lot of built in features.
It can be used as a calculator and for  mathematical operations,
such as statistics, plotting and linear algebra.

This is a fast-track course for high school students with math knowledge.

Students are expected to type and execute cells, and share their results.

You can open this notebook [on jupyter lite](https://jupyter.org/try-jupyter/lab/?fromURL=https://raw.githubusercontent.com/ioggstream/python-course/main/python-high-school/notebooks/00_intro.ipynb).

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
# I can sum, multiply, and modulus (aka, the remainder of the division).
print(a + b, 5 % 2)
```

```python
# I can divide, and elevate to a power.
print(b / a, 2 ** 3)
```

```python
# Brackets are always round.
print(((a + b) * c)/ a + (b *c))
```

----

```python
# Exercise: which is the expected value of 2 * c?
print(2 * c)
```

Exercise: use the cell below to compute the following values:

- the remainder of 12 / 5
- $3 \cdot 8; 2^{10}; 2^{20}; 2^{30}$
- $ \frac{[1 + (1/3 + 1/4)] + 1/5}{6} $

```python
# Use this cell for the exercise.
```

---

**An historical note**

Computers, for performance reasons, use memory in chunks called blocks or pages:
for example, you can't use a single *bit* of memory similarly to how you can't
use a single line of your notebook 📓.

For this reason, it is convenient to use powers of $2^{10}$ to represent the size of files and memory.
They are called "kibi (Ki)", "mebi (Mi)", "gibi (Gi)", etc., to avoid confusion with the powers of $10^{3}$,
which are called
"kilo (k)", "mega (Mi)", "giga (Gi)", and so on.

The unit of measure of information is the *Byte* $B$.
Its multiples can be expressed in powers of $10^3$:

$$
1 kilobyte = 1 kB = 10^3 B = 1000 B
$$

or in powers of $2^{10}$:

$$
1 kibibyte = 1 KiB = 2^{10} B = 1024 B
$$

Exercise:

- how many KiB are in 1KB?

```python
# Use this cell for the exercise.
one_KB = 1e3
one_KB_in_KiB = ...
```

Nowadays it is very important to know the difference between the two units:
when you buy an hard disk of 500GB, you are getting only 465GiB!

----

Exercise:

- you bought a 1TB hard disk: how many bytes can you store on it?

```python
# Use this cell for the exercise.
size_B = ...
```

- How many GiB can you store on it? Hint: reuse the `size_B` variable.

```python
# Use this cell for the exercise.
size_GiB = ...
```

- check the advertised size of your devices (phone, tablet, computer)
  and compute the difference between the one in $GiB$.

```python
# Use this cell for the exercise
```

---

### Representing numbers

A number is represented using digits (in Italian, "cifre"):

- the decimal notation uses 10 digits, from 0 to 9;
- the binary notation uses 2 digits, 0 and 1;
- the octal notation uses 8 digits, from 0 to 7;
- the hexadecimal notation uses 16 digits, where `10` is represented by `A`, `11` by `B`, and so on.

----

A number
represented in base $b$
by the digits $c_0, c_1, c_2, \dots, c_n$
can be computed as:

$
\sum_{i=0}^{n} c_i b^i = c_0 b^0 + c_1 b^1 + c_2 b^2 + \dots + c_n b^n \\
$

Examples:

$
\begin{align}
& 12_{10} = 2 \cdot 10^0 + 1 \cdot 10^1 = 12 \\
& 101_{2} = 1 \cdot 2^0 + 0 \cdot 2^1 + 1 \cdot 2^2 = 5_{10} \\
& 200_{3} = 0 \cdot 3^0 + 0 \cdot 3^1 + 2 \cdot 3^2 = 18_{10} \\
& 9_{16} = 9 \cdot 16^0 = 9_{10} \\
& A_{16} = 10 \cdot 16^0 = 10_{10} \\
& FF_{16} = 15 \cdot 16^0 + 15 \cdot 16^1 = 255_{10} \\
\end{align}
$

Exercise:

- how can I compute the value of the fractional part? Hint: just use the same formula with negative exponents.

$
0.5_{10} = 5 \cdot 10^{-1}
$

- can I compute the value of the following numbers?

$
0.1_{2} = \dots \\
0.5_{2} = \dots
$

----

Python supports the binary, the octal and the hexadecimal notation too!


```python
d = 0b11  # `0b` is the prefix for binary notation
e = 0o11  # `0o` is the prefix for octal notation
f = 0x10  # `0x` is the prefix for hexadecimal (hex) notation
g = 0x1F  # `Remember: hex numbers uses 16 digits, from 0 to F
```

Exercise:

```python
# Use this cell to print the values of d, e, f and g.
```

Questions:

- What is a *bit*?
- What is a *byte*?
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
z, f = c, z + d
```

---
