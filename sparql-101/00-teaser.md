# Knowledge Management 101

Welcome to the Knowledge Management 101 course!
Author: <roberto.polli@par-tec.it>

---

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
%pip install rdflib bokeh networkx
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
from requests import get

g = Graph()
g.parse(data=get("https://dbpedia.org/data/Tortellini.n3").text, format="n3")
plot_graph(g, label_property=RDFS.label, layout=nx.shell_layout, limit=60, filter=".*/dbpedia.org")
```

And we can connect them together

```python
# Extend our graph
g.parse(data=get("https://dbpedia.org/data/Tagliatelle.n3").text, format="n3")

plot_graph(g, label_property=RDFS.label, layout=nx.shell_layout, limit=30, filter=".*/dbpedia.org")
```

Graphs contains a lot of senteces

```python
len(g)
```

but we can query them

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

and see if two resources have something in common...

```python
g.query("""
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?t
WHERE {
        dbr:Tagliatelle ?p1 ?t .
        dbr:Tortellini  ?p2 ?t .
}
"""
).bindings
```
