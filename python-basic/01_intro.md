# Python for System Administrators

Introductory Lesson 2

- Roberto Polli - <roberto.polli@par-tec.it>

```python
# before starting this lesson
#  import the python3 print capabilities
#  using the following statement
#  NB since now you *must* always use
#     parenthesis with print!
from __future__ import print_function, unicode_literals, division
import sys

# Import further python3 features.
if sys.version_info.major < 3:
  from future_builtins import *
  import __builtin__ as builtins
```

## Introducing Lists

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

In python you can create lists of subsequent numbers.
In python 2, the `range` function returns a list,
while in python 3 it returns an iterable object.

This is to avoid memory issues when dealing with large lists.

```python
a = 11
#range in python 2 returns a list
# of consecutive ints
from_0_to_10 = range(a)
l = len(from_0_to_10)
l == a
print(l)
```

```python
# in python 3 things are slightly different
# so the above code won't work.
import sys
if sys.version_info.major < 3:
    range = xrange  # Override the range function with the xrange function.
from_0_to_10 = range(a)
```

```python
# Exercise: can you print the content of from_0_to_10
print(from_0_to_10)
```

```python

# In python 3, you need to create a list from the range object.
# The above code
# should be replaced with the following
from_0_to_10 = list(range(a))
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
f = "prova.txt"
f[:-4], f[-4], f[-3:]
```

```python
# Note: use the os.path module for path manipulation.
# The above code will break with 4-letter extensions!
from os.path import splitext
splitext("prova.foo.yaml")
```

---

## Iterations: for

```python
a_list = ['is', 'iterable', 'with']
for x in a_list:
    print(x)
```

```python
for x in a_list:
    # You need `from __future__ import print_function`
    # for python2 to support the `end` argument
    print((x), end=' ')
    y = x + str(2)
    break       # stop now
```

```python
# what's the expected output of the
# following instruction?
print(("x,y: ", (x, y)))
# Differently from C, `for` does not create
#  a scope
```

---

## Iterations: while

```python
a_list = ['is', 'iterable', 'with']
while a_list:
    # pop() modifies a list removing
    #  and returning its last element
    x = a_list.pop()
    print(("pop out %s" % x))
    break  # what happens if I remove this break?

print(a_list)
```

```python
# What's the expected behavior of the
#  following instructions?
for x in a_list:
    print((x + a_list.pop()))
# for + pop() is not always a good idea ;)
```
