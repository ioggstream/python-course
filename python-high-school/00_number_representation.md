# Representing numbers

## Agenda

- Binary numbers, why should I care?
- Representing numbers in different bases

### Binary numbers, why should I care?

An historical note.

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

A number is represented using digits (:it: "cifre"):
the decimal notation uses 10 digits, from 0 to 9.

----

The value of a number in base $10$ (decimal)
is computed using powers of .. $10$.

$\displaystyle
4 = 4 \cdot 10^0 \\
23 = 3 \cdot 10^0 + 2 \cdot 10^1 \\
105 = 5 \cdot 10^0 + 0 \cdot 10^1 + 1 \cdot 10^2 \\
$

Do you remember that table you learned in primary school?

| number |  k ($10^3$) |  h ($10^2$) |  da ($10^1$) |  u ($10^0$) | Sum |
|-------:|--------------|--------------|--------------|--------------|-----:|
|  23    |      0       |      0       |      2       |      3       |  $3 \cdot 10^0 + 2 \cdot 10^1 + 0 \cdot 10^2 + 0 \cdot 10^3$  |
| 105    |      0       |      1       |      0       |      5       |  $5 \cdot 10^0 + 0 \cdot 10^1 + 1 \cdot 10^2 + 0 \cdot 10^3$  |
| 4321   |      4       |      3       |      2       |      1       |  $1 \cdot 10^0 + 2 \cdot 10^1 + 3 \cdot 10^2 + 4 \cdot 10^3$  |

Exercise:

- can you associate a polynomial to each number in the table above?
- use the `lambda` keyword to associate a polynomial to the number 75

```python
# Use this cell for the exercise.
P_75 = lambda x: 5 * x**0 + 7 * x**1
```

----

#### Other bases

- the binary notation uses 2 digits, 0 and 1;
- the octal notation uses 8 digits, from 0 to 7;
- the hexadecimal notation uses 16 digits, where `10` is represented by `A`, `11` by `B`, and so on.

A number
represented in base $b$
by the digits $c_0, c_1, c_2, \dots, c_n$
can be computed as:

$
\displaystyle
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
