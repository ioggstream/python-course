# Knowledge Management 101

Welcome to the Knowledge Management 101 course!
Author: <roberto.polli@par-tec.it>

---

## Introducing Python

Python is an interpreted, object oriented language with
a lot of built in features.
It can be used as a calculator and for  mathematical operations,
such as statistics, plotting and linear algebra.

This is a fast-track course for high school students with math knowledge.

Students are expected to type and execute cells, and share their results.

You can open this notebook [on jupyter lite](https://jupyter.org/try-jupyter/lab/?fromURL=https://raw.githubusercontent.com/ioggstream/python-course/main/sparql-101/notebooks/00-teaser.ipynb).

---

# Jupyter

Is the course environment in your browser.
It requires a modern browser and an internet connection supporting
websockets. If your network setup (e.g. your proxy)
does not support websockets, you will not be able to
execute the code.

---

While you might find the exercises' solutions in the environment,
it is important for you to spend some time trying to do your homework!
This will help you to remember the concepts and to learn how to use the tools.

---

## What can I do with Jupyter?

You can:

- execute the next cell with `SHIFT+ENTER` (try it now!)

If your environment supports it, you can use features requiring
operating system access:

- [open a (named) terminal on the local machine](/terminals/example)
- [edit an existing file](/edit/notebooks/untitled.txt)

---

- add more cells with `ALT+ENTER`

----

Try to add a cell below this one and write some text in it.

```python
# Add a new python cell with ALT+ENTER.
```

---

## Python terminal

With Jupyter, you have a Python terminal at your disposal.
You can run Python code:

```python
# You can evaluate maths and strings
s = 1
print("a string and the number " + str(s))
```

Jupyter remembers the variables you define in a cell, so you can use them in the next cells.

```python
# Evaluate this cell with SHIFT+ENTER
s = s + 1
print("now s is increased " + str(s))
```

Since Jupyter remembers the variables, you can run the cells in any order you want.
This means that sometimes, you need to "reset" the environment, to start from scratch.

This can be done with the "Kernel > Restart" or "Kernel > Restart & Clear output" menu.

----

## Agenda

- 1h. What is semantics and how to describe information in a
  meaningful (and machine-readable) way using RDF.

- 1h. Storing data or describing knowledge?
  Practical use of getting security insights from data.

- Bonus track: Graphs and semantic search: mixing graphs and vector databases

## Teaser

In this course, we will learn how to describe information in a
machine-readable way using RDF.

```python
%pip install rdflib bokeh
```

For example a person:

```python
from rdflib import Graph
from rdflib.namespace import FOAF, OWL

sentences = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX : <urn:simpsons:>

:Homer foaf:knows :Marge, :Lisa, :Bart, :Maggie;
  foaf:interest <https://dbpedia.org/page/Beer>;
  foaf:name "Homer";

:Lisa foaf:name "Lisa";
  foaf:interest <https://dbpedia.org/page/Jazz> .

"""

g = Graph()
g.parse(data=sentences, format="turtle")
```

Now render a graph

```python
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, from_networkx
from bokeh.models import Circle, MultiLine, Ellipse
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

# Make sure your notebook displays bokeh plots inline
output_notebook()
```

```python
# Convert the RDF Graph to a NetworkX MultiDiGraph
G = rdflib_to_networkx_multidigraph(g)
plot = figure(title="RDF Graph Visualization with Bokeh")

# Convert the networkx graph to a Bokeh graph renderer using the computed layout
graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))
graph_renderer.node_renderer.glyph = Circle(radius=0.06, fill_color="fill_color")
graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

# Add labels
x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
node_labels = [str(g.value(subject=node, predicate=FOAF.name) or node) for node in G.nodes()]
source = ColumnDataSource({'x': x, 'y': y,
graph_renderer.node_renderer.data_source.data['node_label'] = node_labels
                           'node_label': [node_labels[i] for i in range(len(x))]})

labels = LabelSet(x='x', y='y', text='node_label', 
                  source=source,
                  text_font_size="8pt",
                  text_align="center"
                  )
plot.renderers.append(labels)

# Display the plot in the notebook
show(plot)
```