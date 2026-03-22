# Python for High School

 Author: <roberto.polli@par-tec.it>

---

## Introducing Python

Python is an interpreted, object oriented language with
a lot of built in features.
It can be used as a calculator and for mathematical operations,
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

There are basic functions for printing (:it: stampare, from :latin: premĕre) and
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
b = 16.0    # a float (number with decimal part)
```

I can use exponential notation for floats, like $ 1.2 \cdot 10^{2} $

```python
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
# Brackets (parentheses) are always round.
print(
  ((a + b) * c) / a + (b * c)
)
```

Exercise: which of the following expressions is correct?

1. $ \displaystyle \frac{(a+b)}{c} + \frac{b}{a}c $
1. $ \displaystyle \frac{(a+b)c}{a + bc}$
1. $ \displaystyle \frac{\left[(a+b)c\right]}{a} + bc $

:warning: Wrapping a number in parentheses does not change its value:

```python
t = (12)
```

----

```python
# Exercise: which is the expected value of 2 * c?
print(2 * c)
```

Exercise: use the cell below to compute the following values:

- the remainder of 12 / 5
- $\displaystyle 3 \cdot 8; 2^{10}; 2^{20}; 2^{30}$
- $\displaystyle \frac{[1 + (1/3 + 1/4)] + 1/5}{6} $

```python
# Use this cell for the exercise.
```

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

## Simple functions

I can create simple functions using the `lambda` keyword.

```python
# A function that multiplies a number by 2
f = lambda x: x * 2
f(0)
```

Exercise:

- compute `f(0.2)`, `f(1)`, `f(50)`

```python
# Use this cell for the exercise.
f(50)
```

Exercise:

- create a function `p` that computes the polynomial
  $ \displaystyle p(x) = x^2 - 1 $
- compute `p(0)`, `p(1)`, `p(-1)`, `p(3)`

```python
# Use this cell for the exercise.
p = lambda x: ...  # complete the function here
```
