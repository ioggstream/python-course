# Python for High School

Lesson 2

- Roberto Polli - <roberto.polli@par-tec.it>

## Agenda

- Sets
- Introducing Lists
- Getting list items
- Slicing a list
- Strings and Lists
- Iterations: `for`
- Iterations: `while`

## Sets

In maths, a set is a collection of distinct objects.

```python
# In python you can create sets.
EMPTY = {}  # ø is the empty set
A = {1, 2, 3}
B = {3, 4, 5, "a"}  # sets can contain different types
C = { A }   # a set can contain other sets
```

Here is an image from Wikipedia:
[![Set Theory Operations](https://upload.wikimedia.org/wikipedia/commons/0/04/Set_Theory_Operations.svg)](https://en.wikipedia.org/wiki/Set_(mathematics)#/media/File:Set_Theory_Operations.svg)

You can perform set operations on them, including:

$
U = A \cup B \\
I = A \cap B \\
D = A \setminus B \\
S = A \Delta B := (A \cup B) \setminus (A \cap B) \\
$

```python
# Union
U = A | B
# Intersection
I = A & B
# Difference
D = A - B
# Symmetric difference
S = A ^ B
```

You can perform basic checks:

```python
A in U
B not in U
B in D
5 in A
{1} in A
EMPTY in A
I in S
2 in C
```

Exercise: which of the above instructions are true?

```python
# Use this cell for the exercise

```

Exercise: print the content of the sets.

```python
# Use this cell for the exercise

```

## Introducing Lists

A list is an ordered sequence of items.
Differently from a set, a list is ordered
and can contain duplicates.

```python
# it's easy to create a list
list_a = ['this', 'is', 'a', 'list']

```

```python

# you can append items to a list
# with the append method
list_a.append("mutable")
```

```python
# Print its content
print(list_a)
```

```python
# See its length
len(list_a)
```

---

#### Lists and Generators

In python you can generate a sequence of numbers.
To avoid consuming too much memory, this is not doen using lists
or sets, but using special objects that generate those sequences.

```python
a = 11
from_0_to_10 = range(a)
```

Exercise:

- print the length of `from_0_to_10`

```python
# Use this cell for the exercise

```

- print the `type` of `from_0_to_10`

```python
# Use this cell for the exercise

```

We can extract all the elements from a generator using the `list` function.

```python
from_0_to_10 = list(from_0_to_10)
l = len(from_0_to_10)
l == a
print(l)
```


```python
# Exercise: can you print the content of from_0_to_10
print(from_0_to_10)
```


---

## Getting list items

```python
# you can get list items by index
from_0_to_10[0]
```

```python
# Exercise: what happens if I get the 11th element?
from_0_to_10[11]
```

```python
# python is calling under the hood
from_0_to_10.__getitem__(0)
```

Python lists are doubly linked, so you can get the last element using a negative index.

```python
# python lists are doubly linked ;)
from_0_to_10[-1]

```

```python

#  Exercise: please check the manual!
help(list)
```

---

## Slicing a list

```python
straight = [1, 2, 3, 'star']
print(straight)
```

Python supports slicing, that is, getting a subsequence of a list
similarly to what you can do with mathematical intervals.
Python uses a half-open interval
( e.g. $[i, j)$ or $[i, j[$ ),
that is, the first index is included
and the last one is excluded. Given a list `l : |l| = 4`

$
l = [ l_{0}, \dots,  l_{3} ] \\
l[0:2] := [ l_{0}, l_{1} ] \\
l[i:j] := [ l_{i}, \dots, l_{j-1} ] \\
$

This means that the length of a sliced list is:

$
|l[i:j]| = j - i \\
$

```python
# I can take the middle of the list...
straight[1:3]
```

```python
k = 2  # ... or using a separator
straight[0:k], straight[k:4]
```

```python
straight[:k]         # I can omit the first...
```

```python
straight[k:]       # ...and last index
```

---

## Strings and Lists

```python
# Strings behaves like lists
s_a = "Counting: 123"

```

```python

# Have length..
l_a = len(s_a)
print(l_a)
```

```python
# ..indexes
print(s_a[0], " ", s_a[-1])
```

```python
# and a last element
s_a[l_a] # ...what's happening there?
```

```python
# ...we can even slice them
f = "gatto.miao"
f[:-5], f[-5], f[-4:]
```

---

## Juggling with iterables

We can sort and reverse lists.

```python
l = [1, 2, 3, 4, 5]
r = reversed(l)
print(r)
```
reversed is a generator, so we need to convert it to a list to print it.

```python
# Exercise: print the reversed list

```

<!-- print(list(r)) -->

If we have different lists, we can concatenate them.

```python
A = [1, 2, 3]
B = [4, 5, 6]
A + B
```

or associate pairwise elements using the `zip` function.

$
A = [a_0, a_1, a_2]
B = [b_0, b_1, b_2]
diag(A,B) = [ (a_i, b_i) \mid i < min(|A|, |B|) ]
$

```python
D = zip(A, B)
print(D)
```

