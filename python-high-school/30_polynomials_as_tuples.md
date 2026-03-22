# Polynomials as tuples

Abstract: This lesson demonstrates how to multiply
  polynomials in Python. Degree of polynomials is <= 3.

Audience: students with no programming experience,
  of 14 years, at the first year of Italian high school.

## Agenda

- Tuples
- Cartesian Product
- Visualizing cartesian products in 2D
- Polynomials
- Representing polynomials as tuples
- Evaluating polynomials

## Tuples (simplified version)

A python `tuple` (:it: n-pla) is an ordered list of numbers.

```python
# A tuple of 2 elements.
v = (3, 4)
# Another tuple of 2 elements.
w = (-1, 2.5)
```

A tuple can have many elements ...

```python
# A tuple of 3 elements.
p = (1, 0, -2)
# A tuple of 1 element.
q = (5,)
```

... but in this lesson we will use only tuples
of 3 elements.

```python
v = (3, 4, 0)
w = (-1, 2.5, 0)
p = (1, 0, -2)
```

----

I can access the elements of a tuple like this:

```python
# Access the first element of the tuple v
print(v[0])
# Access the second element of the tuple v
print(v[1])
# Access the third element of the tuple v
print(v[2])
# Get the number of elements in the tuple v
print(len(v))
```

In python, tuple indices start from `0`.

| Tuple Index | 0 | 1 | 2 |
|-------------|---|---|---|
| (3, 4, 0)   | 3 | 4 | 0 |

This may seem strange, but it is
just like powers of 10 start from $10^0$,

| Number | $10^0$ | $10^1$ | $10^2$ |
|--------|--------|--------|--------|
| 102    | 1      | 0      | 2      |

and polynomials starts from the constant term

| Polynomial  | $x^0$ | $x^1$ | $x^2$ |
|--------|--------|--------|--------|
| $2x^2 + 0x + 1$ | 1     | 0      | 2      |

and the first button of your elevator is $0$ (the ground floor) ;)

## Polynomials

A polynomial like

 ```math
 P(x) = 3x^2 - 2x + 7
 ```

can be represented as a tuple of its coefficients,
starting from the lowest degree term:

```python
P = (7, -2, 3)
```

where the first element is the coefficient of the highest degree term, and the last element is the constant term.

Exercise: represent the following polynomials
as tuples of coefficients.

:warning: Start from the constant term!

```math
\begin{aligned}
Q(x) &= x - 2\\
R(x) &= -x^2 + 5x + 1\\
S(x) &= 6
\end{aligned}
```

```python
# Use this cell for the exercise.
# Always use 3 elements in the tuple.
Q = ( .., .., ..)
R = ( .., .., ..)
S = ( .., .., ..)
```

## Multiplying polynomials

Try to multiply the following polynomials:

```math
\begin{aligned}
P(x) &= - 2x + 7\\
Q(x) &= x - 2
\end{aligned}
```

What happens if you multiply polynomials
using their tuple representation?

```python
P = (7, -2, 0)
Q = (-2, 1, 0)
```

Can you compute the coefficients
of the resulting polynomial?

```python
PQ = (.., .., ..)
```

## Multiplying tuples

Before continuing with multiplying polynomials,
let's see a way of multiplying tuples:
the Cartesian Product.

If we see tuples as sets, the Cartesian Product of two tuples:

```python
A = (1, 2, 0)
B = (3, 4, 0)
```

$
A \times B = \left\{
  (a; b) :
  \forall a \in A,
  \forall b \in B
\right\}
$

can be expressed in Python as:

```python
AxB = {
  (a,b)
  for a in A
  for b in B
}
print(AxB)
```

| A x B | 3 | 4 | 0 |
|-------|---|---|---|
| 1 | (1,3) | (1,4) | (1,0) |
| 2 | (2,3) | (2,4) | (2,0) |
| 0 | (0,3) | (0,4) | (0,0) |

Exercise:

- modify the code above to compute
the algebraic product of each pair of elements.

```python
A_B = {
  (a * b)
  for a in A
  for b in B
}
print(A_B)
```

| A · B | 3 | 4 | 0 |
|-------|---|---|---|
| 1 | 3 | 4 | 0 |
| 2 | 6 | 8 | 0 |
| 0 | 0 | 0 | 0 |

Exercise:

- match each element in the table above
with the coefficient of the polynomial
multiplication you tried before.

## Back to polynomials

To multiply polynomials represented as tuples,
we can use the same idea of Cartesian Product.

```python
P = (7, -2, 0)  # -2x + 7
Q = (-2, 1, 0)  # x - 2
PQ_terms = {
  (p_deg + q_deg, p_coeff * q_coeff)
  for p_deg, p_coeff in enumerate(P)
  for q_deg, q_coeff in enumerate(Q)
}
print(PQ_terms)
```

Now I need to sum the coefficients
of the same degree.

```python
# Initialize the result polynomial with zeros
PQ = [0, 0, 0, 0]  # degree 3
for deg, coeff in PQ_terms if coeff is not 0:
    PQ[deg] += coeff
print(tuple(PQ))
```
