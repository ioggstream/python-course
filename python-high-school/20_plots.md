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

| x  | f(x)|
|----|-----|
|-10 | -500|
| -9 | -279|
|... | ...|

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

The sympy module has functionalities for geometric objects,
and supports some abstractions like variables and functions.

```python
import matplotlib
from sympy import symbols, Point, Line, Circle, Triangle, Polygon, pi

```

### Plotting a function

```python
# Now the python variable x is a symbolic variable managed by sympy. We can't use it numerically.
x = symbols('x')

# Even functions are symbolic objects when using sympy.
f = x**2 - 2*x + 1

# The `ax` variable represent the cartesian plane.
plot(f, show=True)
```

I can add another function to the same plot

```python
g = 3 - x
# The `ax` variable represent the cartesian plane.
ax = plot(f, g, show=True)
```

I can add further functions using `extend`

```python
h = (x**2 - 1)
ax = plot(f, g, show=False)
ax.extend(plot(h, show=False))
ax.show()
```

sympy supports implicit equations too,
for example the equation of a circle.
These should be plotted using the `plot_implicit` function.

$
\mathcal(C): x^2 + y^2 = 1
$

```python
from sympy import Eq,plot_implicit
x, y = symbols('x y')

# The circle equation
circle = Eq(x**2 + y**2 , 1)

# Prepare a plotted circle
ax = plot_implicit(h, show=False)

# Add the parabola to the plot
ax.extend(plot(f, (x, -2, 2), show=False))

# And finally, show the plot.
ax.show()
```
