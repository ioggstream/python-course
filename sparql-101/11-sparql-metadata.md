# Agenda

- Using SparQL to query metadata

## Metadata, Metadata

Between all triples,
some contain metadata,
such as:

- the resource types (`rdf:type`/`a`, or `rdfs:subClassOf` predicates);
- information about predicates;




```python
from rdflib import Dataset
# Create a dataset...
d=Dataset(store="Oxigraph", default_union=True)

# Bind the namespaces.
d.bind("euvoc", "http://publications.europa.eu/ontology/euvoc#")
d.bind("skos", "http://www.w3.org/2004/02/skos/core#")
d.bind("country", "http://publications.europa.eu/resource/authority/country/")

# Create a graph for the countries.
country = d.graph("http://publications.europa.eu/resource/authority/country")

# Load data into it.
country.parse("countries-skos-ap-act.ttl", format="ox-turtle")
```

And query the simplest metadata:
the `rdf:type`s of the graph's subjects

```python
q = """
SELECT DISTINCT
  ?type
WHERE {
  ?s a ?type .
}
"""
result = country.query(q)

[r.type  for r in result]
```

Since we are returning just `?type`,
we can avoiding gathering `?s`
using the `[]` placeholder.

Try it!


```solution
q = """
SELECT DISTINCT
  ?type
WHERE {
  [] a ?type .
}
"""
result = d.query(q)

[r.type  for r in result]
```

Exercise:

- where can you find the definition of `skos:Concept` and `skos:ConceptScheme`?

<!-- Open the URIRef in your browser -->

----

List `skos:ConceptScheme`s
and their labels.

```python
q = """
SELECT DISTINCT
  ?ConceptScheme
  ?label
WHERE {
  ?ConceptScheme
    a skos:ConceptScheme  ;
    skos:prefLabel ?label .
    # Only English labels
    FILTER (lang(?label) = "en")
}
"""
result = d.query(q)
t = [r.asdict() for r in result]
```

Exercise:

- Rewrite the above query using
  two sentences.

```solution
q = """
SELECT DISTINCT
  ?ConceptScheme
  ?label
WHERE {
  ?ConceptScheme a skos:ConceptScheme .
  ?ConceptScheme skos:prefLabel ?label .
  FILTER (lang(?label) = "en")
}
"""

result = d.query(q)
assert t == [r.asdict() for r in result]
```
----

Now find all the triples
where the `object` is
`<http://publications.europa.eu/resource/authority/country/0005>


```solution
q = """
SELECT DISTINCT *
WHERE {
  ?s ?p <http://publications.europa.eu/resource/authority/country/0005> .
}
"""
result = d.query(q)
[r.asdict() for r in result]
```

Exercise:

- Rewrite the above query using
  the PREFIX directive.

```solution
q = """
PREFIX euvoc: <http://publications.europa.eu/resource/authority/country/>

SELECT DISTINCT *
WHERE {
  ?s ?p ...
}
LIMIT 6
"""
result = d.query(q)
[r.asdict() for r in result]
```

---

Let's visualize the graph
using:

- dotted lines to represent type relations
- parallelograms to represent literals

```mermaid
graph

skos:ConceptScheme
skos:ConceptScheme -->|skos:prefLabel| _l1[/"Concept Scheme"/]

country:0005 -.->|a| skos:ConceptScheme((skos:ConceptScheme))
country:0005 ---|skos:prefLabel| _l[/"Current EU members"/]

country -.->|a| skos:ConceptScheme
country:AUT --->|skos:inScheme| country:0005
country:BEL --->|skos:inScheme| country:0005
country:... --->|skos:inScheme| country:0005

```

----

Now, let's get the predicates associated with resources
of a given type.

```python
q = """
SELECT DISTINCT
  ?type ?p
WHERE {
  [] a ?type ;
     ?p []
  .
  FILTER (?p != rdf:type)
}
"""

result = d.query(q)
{ r.type: r.p for r in result }
```

---

Now, query for the information
associated with the `country:AUT` node.

```python
q = """
PREFIX euvoc: <http://publications.europa.eu/resource/authority/country/>

SELECT DISTINCT *
WHERE {
  country:AUT ?p ?o .

  # Remove blank nodes.
  FILTER(!isBlank(?o))

}
"""

result = g.query(q)
print(*[(r.p.n3(), r.o.n3()) for r in result],sep="\n")
```

Exercise:

- query all skos:Schemes and their labels
  where `country:AUT`
- Hint: use two distinct sentences

<!-- SELECT DISTINCT * WHERE { country:AUT skos:inScheme ?o . ?o skos:prefLabel ?l . } -->

---

**A knowledge graph contains both data and the associated metadata.**
**There isn't a fixed schema, but a set of relations.**
**The actual schema is defined by the ontology and may evolve over time.**

---


Questions:

- List the namespaces registered in the graph.

<!-- list(g.namespaces()) -->

```python
q = """
SELECT DISTINCT *
WHERE {
  [] a ?type .
}
"""
result = g.query(q)
[r.type  for r in result]
```

```python
# For human readable results, bind prefixes.
g.bind("euvoc", "http://publications.europa.eu/ontology/euvoc#Country")
g.bind("country", "http://publications.europa.eu/resource/authority/country/")
to_curie = g.namespace_manager.curie

result = g.query("""
# You always need to bind the prefixes
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>

SELECT DISTINCT *
WHERE {
  ?c a euvoc:Country .
}
LIMIT 3
""")
[to_curie(r.c)  for r in result]
```

Now we will infer how countries are modeled
retrieving all associated predicates,
starting with the types.

We can list all the predicates
associated with `euvoc:Country`,
thus inferring how countries are modeled.

The fact that every property is defined by
an URI allows us to use
the same property in different contexts.

```python
q = """
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>
PREFIX country: <http://publications.europa.eu/resource/authority/country/>

SELECT DISTINCT *
WHERE {
  [] a euvoc:Country ;
     a ?type .
}
"""
result = g.query(q)
country_types = {r.type for r in result}
```

The data model extracted from the graph:
subjects in the country:0005 ConceptScheme
inherit properties from both `euvoc:Country`
and `skos:Concept`.

```mermaid
graph LR

country:... --->|skos:inScheme| country:0005

country:... -.->|a| euvoc:Country & skos:Concept

skos:Concept -.->|a| rdfs:Class
euvoc:Country -.->|a| rdfs:Class
euvoc:status -->|rdfs:domain| euvoc:Country
skos:prefLabel -->|rdfs:domain| skos:Concept

```
