# Graph databases & SparQL

## Agenda

- Storing and retrieving triples
- Virtuoso
- GraphDB

*Beware*: commands may contain small typos. You must fix them to properly complete the course!

----

Prerequisites:

- JSON, YAML, xmlschema
- HTTP, OpenAPI 3
- SQL and database hints

---

## Graphs (again)

### RDF databases

An RDF graph is an (unordered) set of triples.

Each triple consists of a `subject`, `predicate`, `object`.

Graph databases such as:

- [Virtuoso (opensource)](https://virtuoso.openlinksw.com/),
- [GraphDB (proprietary)](),
- [Amazon Nepture (proprietary SaaS)]()

store triples into graphs.

They can be queried using the [SparQL]() language.


----

### Non-RDF databases: Neo4j

Another notable graph database is [Neo4j (opensource)]().

It is not a triple store, and it
adopt a different approach named [Labeled Property Graphs](https://en.wikipedia.org/wiki/Labeled_property_graph)

Neo4j can be queried with the [Cypher](https://neo4j.com/developer/cypher-query-language/) language.

Neo4j supports RDF datasets via the Neosemantics plugin.

----

## rdflib backends

We will simulate a graph database using
[rdflib](https://rdflib.readthedocs.io/en/stable/index.html),
that supports SparQL queries.

rdflib supports multiple backends to parse and store triples.

oxrdflib is a performant one
based on [Oxigraph](https://github.com/oxigraph/oxigraph).

```python
%pip install oxrdflib
```

Let's test it.

```python
from rdflib import Graph

g = Graph()

# Use the default backend.
%time g.parse("countries-skos-ap-act.ttl", format="text/turtle")
print("The graph contains", len(g), "triples.")
```

```python
g=Graph(store="Oxigraph")

# Use the ox-turtle parser.
%time g.parse("countries-skos-ap-act.ttl", format="ox-turtle")
print("The graph contains", len(g), "triples.")
```

See also:

- <https://rdflib.readthedocs.io/en/stable/persistence.html>

---

## SparQL practice

Let's load into it the [European vocabulary for countries](countries.ttl).

See also:

- [EU Authority Tables](https://op.europa.eu/en/web/eu-vocabularies/authority-tables)

```python
from rdflib import Graph

# Let's create a graph.
g = Graph(store="Oxigraph")

# And load into it the European
# vocabulary for countries.
g.parse("countries-skos-ap-act.ttl", format="ox-turtle")
```




---

### Traversing the graph

The Country graph contains more than countries.

```python
to_curie = g.namespace_manager.curie

q = """
PREFIX country: <http://publications.europa.eu/resource/authority/country/>

SELECT DISTINCT *
WHERE {
  country:ITA skos:narrower ?narrower .
  ?narrower skos:prefLabel ?label .
  FILTER (lang(?label) = "en")
}
"""
result = g.query(q)

narrower = {to_curie(r.narrower): str(r.label) for r in result}

print(*narrower.items(), sep="\n")
```

Exercise:

- run the above query replacing `skos:narrower` with `skos:narrower*`;
  what happens?
- run the above query using `country:FRA` and see what happens;
  then replace `skos:narrower` with `skos:narrower/skos:narrower`:
  do you see the same number of results?

<b>
The `*` operator is used to traverse the graph
and find all the nodes reachable from the starting node.
The `*` operator is not supported by all graph databases.
</b>

#### Creating a graph

SparQL can create new graphs from an existing one.

```sparql
q = """
PREFIX country: <http://publications.europa.eu/resource/authority/country/>

CONSTRUCT {
  ?narrower
    skos:prefLabel ?label ;
    skos:broader ?broader .
}
WHERE {
  ?narrower
    # All resources transitively related to country:FRA...
    skos:broader* country:FRA ;

    # ... with their labels ...
    skos:prefLabel ?label ;

    # ... and their broader relations.
    skos:broader ?broader .

  FILTER (lang(?label) = "en")
}
"""
result = g.query(q)
list(result.graph)
```

Let's visualize the graph.

```python
from tools import plot_graph
from rdflib import SKOS

plot_graph(result.graph, label=SKOS.prefLabel)
```

#### More metadata

The Country graph contains more than countries ;)
the resource type is identified by the `lemon:context` property.

```python
q = """
PREFIX lemon: <http://lemon-model.net/lemon#>
PREFIX country: <http://publications.europa.eu/resource/authority/country/>
PREFIX context: <http://publications.europa.eu/resource/authority/use-context/>

SELECT DISTINCT
  ?broader
  (COUNT(?narrower) AS ?count)
WHERE {
  ?broader
    skos:narrower+ ?narrower ;

    lemon:context context:COUNTRY ;

    # ... with their labels ...
    skos:prefLabel ?label .


  FILTER (lang(?label) = "en")
}
GROUP BY ?broader
ORDER BY ?count
"""
result = g.query(q)
list(result)
```

---

## Datasets

An RDF dataset is made of multiple graphs.

```python
from rdflib import Dataset

d = Dataset(store='Oxigraph')
# Add ns shortcuts.
d.bind("eu", "https://publications.europa.eu/resource/authority/")
d.bind("schema": "https://schema.org/")
d.bind("euvoc": "http://publications.europa.eu/ontology/euvoc#")



d.graph(identifier="urn:People").parse(data=json.dumps(nodes_ld), format="application/ld+json")
d.graph(identifier="eu:country").parse("countries-skos-ap-act.ttl", format="ox-turtle")
[len(x) for x in d.graphs()]
```
