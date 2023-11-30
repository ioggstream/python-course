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
```

Exercise: which of the above expressions are true?

```python
#  Make an hypothesis first, then check it using this cell.

```

```python
{1} in A
EMPTY in A
I in S
2 in C
```

Exercise: which of the above expressions are true?

```python
#  Make an hypothesis first, then check it using this cell.

```

Exercise: print the content of the sets.

```python
# Use this cell for the exercise

```

## Tuples (Vectors)

A python `tuple` (:it: n-pla) represents an ordered list of objects,
and can contain duplicates.

They seem like vectors,

$
\underline{v} = (v_0, v_1, \dots, v_n) \in \mathbb{R}^n
$

but they are not!

Here are two tuples in $\mathbb{R}^2$:

```python
v = (0, 0)
w = (3, 4)
```

Exercise: print the content of the tuples.

```python
print(v[0])
```

Beware: operations on tuples are not the same as operations on vectors!

```python
# Exercise: try to sum and multiply v and w. Which is the result? What would you expect?

```

Exercise: try to modify the first element of v. What happens?

```python
# Use this cell for the exercise

```

Tuples are immutable!

## Introducing Lists

A list is an **ordered** sequence of objects.
Differently from a set, a list is ordered
and can contain duplicates.

```python
# it's easy to create a list
list_a = ['this', 'is', 'a', 'list']

```

```python
# you can append objects to a list
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

The `range` function generates a sequence of numbers.
To avoid consuming too much memory, this is not done using lists
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
# Exercise: print the content of from_0_to_10

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
type(straight)  # This is a list!
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

## Juggling with collections

We can sort and reverse lists.

```python
l = [1, 2, 3, 4, 5]
r = reversed(l)
print(r)
```

reversed is a generator, so we need to "materialize" it into a list to print it.

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

create the cartesian product of two lists.

$
A \times B := \{ (a; b) \mid a \in A, b \in B \}
$

|AxB|   |   |   |
|---|---|---|---|
| | 1, 4 | 1, 5 | 1, 6 |
| | 2, 4 | 2, 5 | 2, 6 |
| | 3, 4 | 3, 5 | 3, 6 |

```python
AxB = [(a, b) for a in A for b in B]
```

or associate pairwise elements using the `zip` function.

|$A \Delta B$|   |   |   |
|---|---|---|---|
| | 1, 4 |      |      |
| |      | 2, 5 |
| |      |      | 3, 6 |

$
A = [a_0, a_1, a_2] \\
B = [b_0, b_1, b_2] \\
A\DeltaB = [ (a_i; b_i) \mid i < min(|A|, |B|) ]
$

```python
D = zip(A, B)
print(D)
```

Exercise: can you materialize the zip object into a list?
<!-- D = list(D) -->

```python
# Use this cell for the exercise

```


## The itertools module

The itertools module provides advanced tools for working with collections.

```python
import itertools
from itertools import product, permutations, combinations
```

You can create combinations, permutations, and cartesian products.

```python
A = [1, 2, 3]
B = [0, 1]
n = len(A)
k = 2
```

```python
AxB = product(A, B)
P_A = permutations(A)
C_A_2 = combinations(A, k)
```

Exercise: print the content of the above objects.

```python
# Use this cell for the exercise

```

Combinations are useful to generate all the possible subsets of a set
of a given size.

Can you fix the expression below and compute its value?

<!-- len(permutations(A)) == math.factorial(l) -->
<!-- r == math.factorial(k)*math.factorial(n-k) -->

```python
r = len(P_A) / len(C_A_2)
```
