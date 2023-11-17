# Python for High School

Lesson 3: Iterations

## Agenda

- Conditions: `if`
- Iterations: `for`
- Iterations: `while`


## Conditions: `if`

Python can evaluate conditions using `if` statements.

```python
n = 2
parity = "even" if n % 2 == 0 else "odd"
```

More complex conditions can be evaluated using multiple lines
and the `elif` and `else` keywords.

```python
# Sign of a function.
n = 1
if n > 0:
    sign = 1
elif n < 0:
    sign = -1
else:
    sign = 0
```

```python
# Exercise. Modify the cell above and check that the sign of 0 is 0.
print(sign)
```

## Iterations: `for`

Iterating means to repeat a process multiple times
with different values.

We are familiar with iterations in maths.
When we sum a list of numbers, we always repeat the same process:

0. start with a sum of 0
1. take the next number from the list
2. add it to the sum
3. if there are more numbers, go to 1
4. otherwise, stop

Python allows you to iterate over a sequence of items using the `for` instruction.

```python
a_list = ['is', 'iterable', 'with']
for x in a_list:
    print(x)
```

We can stop the iteration using the `break` instruction.

```python
for x in a_list:
    print(x, end=' ')
    y = x + str(2)
    break       # stop now
```


```python
# what's the expected output of the
# following instruction?
print(("x, y: ", (x, y)))
# Differently from other languages like C, `for` does not create
#  a scope
```

Combining `if` and `break` we can stop the iteration when a condition is met.

```python
for i in range(10):
    if i == 5:
        break
    print(i, end=' ')
```

We can use conditions on other variables

```python
s = 0
for i in range(10):
    if s > 10:
        break
    s += i
print(s, end=' ')
```

Exercise: write a loop that prints all the divisors of $n=100$.

```python
n = 100
for q in range(2, n):
    # Write your code here.
    
```

---

## Iterations: while

We can even iterate over specific conditions.

```python
i = 10:
while i > 0:
    print(i, end=' ')
    i -= 1
```

Exercise: complete the code below to write a loop with the same output of the previous cell.

```python
i = ...
while ...:
    print(i, end=' ')
    i += 1
```

Exercise: write a loop that prints all the divisors of $n=100$.

```python
n = 100
q = 2
while ...:
    if ...:
        print(q, end="; ")
    ...    
```

Exercise: write a loop that prints all the prime factors of $n=100$, i.e. $2; 2; 5; 5;$.

```python
n = 100
q = 2
while ...:
    if ...:
        print(q, end="; ")
    ...

```
<!-- 
n = 100
q = 2
while n>1:
    if n%q == 0:
        print(q, end="; ")
        n //= q
    else:
        q += 1 -->
---

`while` can use an iterable to check if there are more elements.


```python
a_list = ['is', 'iterable', 'with']
while a_list:
    # pop() modifies a list removing
    #  and returning its last element
    x = a_list.pop()
    print(f"pop out {x}")
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

