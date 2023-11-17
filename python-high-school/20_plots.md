# Plotting

Python can plot data and functions with the `matplotlib` module.

```python
import matplotlib.pyplot as plt
import math
```

A computer can't plot a function, it can only plot points. So we need to provide a set of points that are close enough to the function.
This means that when you zoom in, the plot looks like a series of joint segments.

## Plotting points

We can use the `lambda` keyword to define simple functions.
This is equivalent to

$
f(x) = x^3 - 50x
$

```python
f = lambda x: x**3 - 50 * x
```

Now define a domain range and evaluate the function

$
\mathcal{D} = [-10; 10 ] \cap \mathbb{Z} \\
\mathcal{C} = f(\mathcal{D}) := \{f(x) \mid x \in \mathcal{D} \}
$

```python
D = list(range(-10,10))
C = [f(x) for x in D]
```

Exercises:

- print the domain and codomain

```python
# Use this cell for the exercise

```

- use the `zip` function to print a table pairs
  using the string formatting tools, e.g.:

~~~
 x  | f(x)
-10 | -500
 -9 | -279
... | ...
~~~

<!-- list(zip(C, D)) -->
```python
# Use this cell for the exercise

```

Now we can plot the function providing the two sets

```python
# add axis
plt.axhline(0, color='black')
plt.plot(D, C)
```

## Geometric plotting

The sympy module has functionalities for geometric objects.

```python
import matplotlib
from sympy import symbols, Point, Line, Circle, Triangle, Polygon, pi

```