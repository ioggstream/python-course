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

```python
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
plot_graph(g, label_property=RDFS.label, limit=30, pattern=".*/dbpedia.org")
```

And we can connect them together

```python
# Extend our graph
g.parse(data=get("https://dbpedia.org/data/Tagliatelle.n3").text, format="n3")

plot_graph(g, label_property=RDFS.label, limit=50, pattern=".*/dbpedia.org")
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
  ?s
    a   dbo:Food ;
    ?p  dbr:Italy .
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
  ?subject
    a dbo:Food ;
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
  ?URI
    skos:inScheme euvoc:country ;
    dc:identifier ?identifier ;
    skos:prefLabel ?concept
  .

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

More relations

```python
from tools import plot_graph
import networkx as nx
ret = eu.query("""
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>


CONSTRUCT   {

?s skos:narrower ?q

}
WHERE {

?s skos:inScheme <http://data.europa.eu/nuts/scheme/2024> ;
skos:narrower ?q ;
               <http://data.europa.eu/nuts/level> "0"
.
}
LIMIT 400
""")


plot_graph(ret.graph, layout=nx.planar_layout)
```

---

## Transform kube infra in graph

```python
% pip install d3fendtools
```

---

List Basic attacks on your kube infrastructure

```python
from rdflib import Graph
from tools import plot_graph

kube = Graph()
kube.parse('guestbook.ttl', format="text/turtle")

# Simplify the graph ;)
for s, p, q in kube:
    if 'urn:k8s:default' in str(s):
        continue
    if str(s).startswith(("urn:k8s:", "rdfs:", "rdf:")):
        kube.remove((s, p, q))
    if str(q).startswith(("urn:k8s:", "rdfs:", "rds:")):
        kube.remove((s, p, q))

plot_graph(kube)
```

Get security insights from the NSA knowledge graph.

```python
kube=Graph()
kube.parse('guestbook.ttl', format="text/turtle")
kube.parse('d3fend.ttl', format="text/turtle")
kube.query("""
SELECT DISTINCT *
WHERE {
  ?artifact rdfs:subClassOf d3f:DigitalArtifact
}
""")
```

and apply this stuff to our infrastructure.

```python

attack_surface = list(kube.query("""
SELECT DISTINCT
  ?attack_label ?affects ?artifact ?uri
WHERE {
  ?kind rdfs:subClassOf* d3f:DigitalArtifact .
  ?kind rdfs:subClassOf* k8s:Kind .
  ?kind rdfs:subClassOf ?artifact .

  ?attack
    d3f:attack-id ?attack_id;
    rdfs:label ?attack_label .

  ?attack ?affects ?artifact .
  ?uri a ?kind .

}
"""))

print('\n'.join(sorted([
    (f"Attack: {a['attack_label']},"
     f" {a['affects'].fragment} {a['artifact'].fragment} for {a['uri']}")
    for a in attack_surface
])))
```
