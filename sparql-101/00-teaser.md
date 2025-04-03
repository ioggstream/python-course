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
%pip install rdflib
```

(and some graph libraries)

```python
%pip install bokeh
```

``python
%pip install networkx
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

Graphs contain a lot of senteces

```python
len(g)
```

but we can query them (e.g., for Italian food)

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

We can query remote graphs (e.g., DBPedia):

```python
dbpedia = Graph(store="SPARQLStore")
dbpedia.open("https://dbpedia.org/sparql")

dbpedia.query("""
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?subject ?label
WHERE {
    ?subject a dbo:Food ;
             rdfs:label ?label
    FILTER (lang(?label) = 'en')
    .
}
LIMIT 10
""").bindings
```

Provided by different organizations

```python
eu = Graph(store="SPARQLStore")
eu.open("https://publications.europa.eu/webapi/rdf/sparql")

eu.query("""
PREFIX euvoc: <http://publications.europa.eu/resource/authority/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?URI, ?concept, ?identifier
WHERE {
 ?URI skos:inScheme euvoc:country ;
 skos:prefLabel ?concept ;
 dc:identifier ?identifier
 FILTER(lang(?concept) = 'en')
}
LIMIT 5

""").bindings
```

And their relations

```python
eu.query("""
PREFIX euvoc: <http://publications.europa.eu/resource/authority/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>

# Construct a graph of countries and their identifiers related by dct:replaces
# countries must be in the euvoc:country scheme.

CONSTRUCT { ?a dct:replaces ?b}
WHERE {
 ?a skos:inScheme euvoc:country.
 ?b skos:inScheme euvoc:country.
 ?a dct:replaces ?b .
}

LIMIT 5

""").bindings
```
