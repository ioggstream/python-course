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

For example network of persons:

```python
from rdflib import Graph
from rdflib.namespace import FOAF, OWL

sentences = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX : <urn:simpsons:>

:Homer foaf:knows :Marge, :Lisa, :Bart, :Maggie;
  foaf:interest <https://dbpedia.org/page/Beer>;
  foaf:firstName "Homer".

:Lisa foaf:firstName "Lisa";
  foaf:interest <https://dbpedia.org/page/Jazz> .

"""

g = Graph()
g.parse(data=sentences, format="text/turtle")
```

... eventually rendered as a graph ...

```python
from tools import plot_graph
plot_graph(g, label_property=FOAF.firstName)
```

Convert it in [JSON-LD](https://json-ld.org/) format:

```python
json_text = g.serialize(format="application/ld+json")
print(json_text)
```

There's plenty of knowledge in the web!

```python
from rdflib import Graph
from rdflib.namespace import RDFS
import networkx as nx

g = Graph()
g.parse("https://dbpedia.org/data/Tortellini.n3", format="n3")
plot_graph(g, label_property=RDFS.label, layout=nx.shell_layout, limit=60, filter=".*/dbpedia.org")
```

And we can connect them together

```python
# Extend our graph
g.parse("https://dbpedia.org/data/Tagliatelle.n3", format="n3")

plot_graph(g, label_property=RDFS.label, layout=nx.shell_layout, limit=30, filter=".*/dbpedia.org")
```

We can also query the graph for Italian food

```python
g.query("""
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?s
WHERE {
        ?s a dbo:Food ;
           ?p dbr:Italy .
}
"""
).bindings
```

Or ask what do some items have in common

```python
g.query("""
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?t
WHERE {
        ?s a dbo:Food .
        ?q a dbo:Food .
        ?s ?p ?t .
        ?q ?p ?t .
        FILTER (?s != ?q)
}
"""
).bindings
```
