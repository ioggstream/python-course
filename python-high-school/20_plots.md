# Plotting

Python can plot data and functions with the `matplotlib` module.

```python
import matplotlib.pyplot as plt
import math
```

Let's define a simple function

```python
f = lambda x: x**3 - 50 * x
```

Now define a domain range and evaluate the function

$$
\mathcal{D} = [-10; 10 ] \cap \mathbb{Z} \\
\mathcal{C} = f(\mathcal{D}) := \{f(x) \mid x \in \mathcal{D} \}
$$

```python
D = list(range(-10,10))
C = [f(x) for x in D]
```

Now we can plot the function providing the two sets

```python
# add axis
plt.axhline(0, color='black')
plt.plot(D, C)
```
