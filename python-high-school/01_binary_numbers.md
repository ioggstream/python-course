# More on numbers

Audience: students with no programming experience,
  but with knowledge of decimal and binary notation,
  polynomials, logic operations and basic set theory.

## More on binary numbers

We can use f-strings to print the binary representation of a number.
The pattern is `{variable:format specification}`.
In the code below:

- the variable is `a`
- the format specification is `#b` (binary with the `0b` prefix).

```python
a = 3
print(f"{a:#b} is the binary representation of {a}")
```

Exercise: print the binary representation of the following numbers:
  3, 61, 35.

<!-- Solution -->
<!-- print(f"{3:#b}") -->
<!-- print(f"{61:#b}")-->
<!-- print(f"{35:#b}")-->

```python
# Write your code here.
```

Exercise: what happens if you remove the `#` in the format specification?

```python
# Use this cell for the exercise.

```

To align the number representations, we can specify their length (e.g., 10 characters).

```python
a = 3
print(f"{a:#10b} is the binary representation of {a}")
a = 61
print(f"{a:#10b} is the binary representation of {a}")
```

I can also specify to fill the empty spaces with `0`s.

```python
a=3
print(f"{a:#010b} is the binary representation of {a}")
a=61
print(f"{a:#010b} is the binary representation of {a}")
```

In this way I can easily compare the binary representations of two numbers.

| number |  $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|--------|-------|-------|-------|-------|-------|-------|-------|-------|
| 3      | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 1     |
| 61     | 0     | 0     | 1     | 1     | 1     | 1     | 0     | 1     |

----

### Bitwise operators: `<<` and `>>`

Bitwise operators are the most simple operators,
since they operate on single digits.
They are used to manipulate the binary representation of numbers.

- Exercise on the `<<` (left-shift) operator: given the following number

```python
a = 1
```

try to guess the result of the following operations. Hint: execute the cell below multiple times.

```python
a = a << 1
print(f"{a:#010b}")
```

Is there a similar operator with numbers in base 10?

- Exercise on the `>>` (right-shift) operator: given the following number

```python
a = 79
```

try to guess the result of the following operations. Hint: execute the cell below multiple times.

```python
a = a >> 1
print(f"{a:#010b}")
```

Is there a similar operator with numbers in base 10?

Discuss the results with your classmates.

### Bitwise operators: AND `&`

The `&` operator is the bitwise AND operator.
It returns 1 if both bits are 1, 0 otherwise.

```python
a = 19
b = 61
c = a & b
print(f"{a:#010b}")
print(f"{b:#010b}")
print(f"{c:#010b}")
```

| number |  $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|--------|-------|-------|-------|-------|-------|-------|-------|-------|
| 19      | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 1     |
| 61     | 0     | 0     | 1     | 1     | 1     | 1     | 0     | 1     |
| 19 & 61 | 0     | 0     | 0     | 1     | 0     | 0     | 0     | 1     |

The AND operator has a physical meaning: it is used to check if, in a circuit, two switches are both ON.

- 🔋--1--1--💡ON
- 🔋--0--1--💡OFF
- 🔋--1--0--💡OFF
- 🔋--0--0--💡OFF

[![](https://mermaid.ink/img/pako:eNplkU9rwzAMxb-K8amFepAecxgM2p66Dbbb6h78R0kMjp0pMqOUfvc5TsIO00nS-_F4SHduogVe88bHH9MpJHb-kGFMukU1dOzl7XA5ejCEzjDj0CRHVxmsw7xzMRSa5dKiujSqbpTQigjwJqhDAPGdsifgeJ0xD7aAOJHetR3p5DV7P50WYKxEtdnMThTb1oOITbPdLur-vxpWMUdgQojn4vHntuz2a1cizLJ4yrOeJghWBr7jPWCvnM0HuU-I5NRBD5LXubXQqORJchkeGU2DVQRH6ygirwkT7LhKFD9vwazzzBycytfseU7tx7wdVPiKsV8hKBav8x_KOx6_iymCQQ?type=png)](https://mermaid.live/edit#pako:eNplkU9rwzAMxb-K8amFepAecxgM2p66Dbbb6h78R0kMjp0pMqOUfvc5TsIO00nS-_F4SHduogVe88bHH9MpJHb-kGFMukU1dOzl7XA5ejCEzjDj0CRHVxmsw7xzMRSa5dKiujSqbpTQigjwJqhDAPGdsifgeJ0xD7aAOJHetR3p5DV7P50WYKxEtdnMThTb1oOITbPdLur-vxpWMUdgQojn4vHntuz2a1cizLJ4yrOeJghWBr7jPWCvnM0HuU-I5NRBD5LXubXQqORJchkeGU2DVQRH6ygirwkT7LhKFD9vwazzzBycytfseU7tx7wdVPiKsV8hKBav8x_KOx6_iymCQQ)


- Exercise: compute the bitwise AND of 192 and 71 by hand and check the result in the cell below.

<!-- solution: a, b = 192, 71; c = a & b; print(f"{a:#010b}"); print(f"{b:#010b}"); print(f"{c:#010b}"); -->

```python
# Write your code here.

```

### Bitwise operators: OR `|`

The `|` operator is the bitwise OR operator.
It returns 1 if at least one bit is 1, 0 otherwise.

```python
a = 6
b = 5
c = a | b
print(f"{a:#010b}")
print(f"{b:#010b}")
print(f"{c:#010b}")
```

| number |  $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|--------|-------|-------|-------|-------|-------|-------|-------|-------|
| 6      | 0     | 0     | 0     | 0     | 0     | 1     | 1     | 0     |
| 5      | 0     | 0     | 0     | 0     | 0     | 1     | 0     | 1     |
| 6 \| 5 | 0     | 0     | 0     | 0     | 0     | 1     | 1     | 1     |

- Exercise: compute the bitwise OR of 192 and 71 by hand and check the result  in the cell below.

<!-- solution: a, b = 192, 71; c = a | b; print(f"{a:#010b}"); print(f"{b:#010b}"); print(f"{c:#010b}"); -->

The OR operator has a physical meaning: it is used to check if, in a circuit, at least one switch is ON.

[![](https://mermaid.ink/img/pako:eNpdkL1uAyEQhF8FbRHZkolkl1ekSro4luLOIQUcyx0SBxdYFFmW3z17P25CtcN8zIq5QZssQgMupN-215nE-6eKKpZquqzHXpxYWp-xJZ_ibAo-5svpxmlpNBHmq6Q-I8qfygGYy_cKCSnliyh78STKYREBrZDPPJiFYc1RZcoKvuvJ1GDE6WNNKPvNZllEqesCyhS329U6_LecmzyMVkXYwYB50N7y127TAwXU44AKGh4tOl0DKVDxzmgdrSZ8s55ShoZyxR3oSul8je1DL8yr19zKALw2FL4ddbykNDwgnCOOS6Nzsfc_f7R0Qw?type=png)](https://mermaid.live/edit#pako:eNpdkL1uAyEQhF8FbRHZkolkl1ekSro4luLOIQUcyx0SBxdYFFmW3z17P25CtcN8zIq5QZssQgMupN-215nE-6eKKpZquqzHXpxYWp-xJZ_ibAo-5svpxmlpNBHmq6Q-I8qfygGYy_cKCSnliyh78STKYREBrZDPPJiFYc1RZcoKvuvJ1GDE6WNNKPvNZllEqesCyhS329U6_LecmzyMVkXYwYB50N7y127TAwXU44AKGh4tOl0DKVDxzmgdrSZ8s55ShoZyxR3oSul8je1DL8yr19zKALw2FL4ddbykNDwgnCOOS6Nzsfc_f7R0Qw)

---
