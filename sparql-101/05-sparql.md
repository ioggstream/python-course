# SparQL 101

## Agenda

- Storing and retrieving triples

*Beware*: commands contain small typos. You must fix them to properly complete the course!

---

Prerequisites:

- json, yaml, xmlschema
- HTTP, OpenAPI 3
- SQL and database hints

---

## Querying graphs with SparQL

An RDF graph is an (unordered) set of triples.

Each triple consists of a `subject`, `predicate`, `object`.

An RDF dataset is a collection of graphs.

SparQL is a query language for RDF datasets.

See: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#dataset

```python
from rdflib import Dataset
d = Dataset()
```

----

A sparql query retrieves all entries
matching one or more sentences

```raw
SELECT *
WHERE {
  ?subject ?predicate ?object .
  # ... more sentences ...
}
```

This workshop provides a non-exhaustive introduction to SparQL.

----

### Sparql: the _:sample graph

Open [sample.ttl](sample.ttl) in another tab
and see its content.

Now load into the dataset.

```python
g = d.graph("_:sample")
g.parse("sample.ttl", format="text/turtle")
```

Use our utility function to print the graph.

```python
import tools
tools.plot_graph(g, label_property=FOAF.name)
```

List all entries

```python
q = """
SELECT *
WHERE {
  ?subject ?predicate ?object .
}
LIMIT 2
"""
result = g.query(q)
[r.asdict() for r in result]
```

Exercise:

- Remove the `LIMIT` clause.
  How many triples are in the graph?

```python
# Use this cell for the exercise.

# You can use variable names.
for r in result:
    print(r.subject, r.predicate, r.object, sep="\t")

```

- Replace `?subject` with `?foo`:
  what happens?

----


SparQL can correlate
entries using semantically defined
vocabularies such as FOAF.

:warning: The `PREFIX` statement in a sparql query
must not have a trailing dot, because it is not a sentence.
This is different from the `@prefix` statement
in turtle.

```python
q = """
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

SELECT * WHERE {
  ?s foaf:name ?o .
}
"""

result = g.query(q)
[r.asdict() for r in result]
```

In this case `foaf:name` has a very specific meaning.
You don't need to create indexes in your database
to search for specific predicates.

Exercise:

- What happens if you add a dot at the end of the `PREFIX` statement
  in the above query?

----

Graph databases have an inference engine that can be used
to process complex queries.

```python
q = """
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

SELECT *
WHERE {
  ?s a foaf:Person  .
  ?s foaf:knows ?o  .
}
"""

result = g.query(q)
[r.asdict() for r in result]
```

The `*` operator matches a predicate
0 or more times.
This allows to find all
the friends' network of a person.

Exercise:

- modify the above query replacing `foaf:knows` with `foaf:knows*`
  and see what happens.

SparQL supports GROUP BY and ORDER BY clauses.

```python
q = """
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT
  ?s
  (GROUP_CONCAT(?o; separator=", ") AS ?friends)
WHERE {
  ?s
    a foaf:Person ;
    foaf:knows* ?o
  .
}
GROUP BY ?s
"""
result = g.query(q)
{str(r.s): {"network": str(r.friends) } for r in result}
```

----

Using multiple lines we can infer things
such as friend-of-a-friend emails.

```python
q = """
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT
  ?mail1 ?mail3
WHERE {
  ?user1 foaf:knows ?user2
  .
  ?user2 foaf:knows ?user3
  .
  ?user1 foaf:mbox ?mail1
  .
  ?user3 foaf:mbox ?mail3
}
"""

result = g.query(q)
[r.asdict() for r in result]
```

Since we are not interested in the `user2` variable,
we can simplify the query specifying
a path of predicates.

```python
q = """
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT
  ?mail1 ?mail3
WHERE {
  ?user1 foaf:knows/foaf:knows ?user3
  .
  ?user1 foaf:mbox ?mail1
  .
  ?user3 foaf:mbox ?mail3
}
"""
result = g.query(q)
{str(r.mail1): str(r.mail3) for r in result}
```

----

Note that the query describes each relation
ignoring the way data is stored.

---

# Querying DBPedia

:warning: DBPedia may rate limit your queries.

[DBPedia](https://dbpedia.org/sparql) is a graph database with a lot of data inside.

We can use it to learn sparql.

- list concepts

```text
SELECT DISTINCT
  ?Concept
WHERE {
  [] a ?Concept
}
LIMIT 20
```

----

Now we want to list all `Person`

```text
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT
  *
WHERE {
  ?s a foaf:Person
}
LIMIT 10
```

----

All `Person`s born in Pisa

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT
 *
WHERE {
  ?s a foaf:Person .
  ?s dbp:birthPlace dbr:Pisa
}
LIMIT 10

```

... with their deathplaces

```raw
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>


SELECT DISTINCT *
WHERE {
  ?s a foaf:Person .
  ?s dbp:birthPlace dbr:Pisa .
  ?s dbp:deathPlace ?death_place
}
LIMIT 10
```

----

If deathplace is in UK

```raw
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT * WHERE {
  ?s a foaf:Person .
  ?s dbp:birthPlace dbr:Rome .
  ?s dbp:deathPlace ?deathPlace .
  ?deathPlace dbo:country dbr:United_Kingdom
}
LIMIT 50

```

----

We can extend the search to every person
born in Italy and dead in UK:

- replacing `dbr:Rome` with `?birth_place`
- restricting `?birth_place` to `dbr:Italy`

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT *
WHERE {
  ?s a foaf:Person .
  ?s dbp:birthPlace ?birth_place .
  ?s dbp:deathPlace ?deathPlace .

  ?deathPlace dbo:country dbr:United_Kingdom .
  ?birth_place dbo:country dbr:Italy
}
LIMIT 50
```

----

There's no theoretical ;) limit to the inference, for example
we could require that the birthplace of that
person should match the one of a Pope.

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT * WHERE {
  ?s a foaf:Person .
  ?s dbp:birthPlace ?birth_place .
  ?birth_place dbo:country dbr:Italy .
  ?s dbp:deathPlace ?death_place .
  ?death_place dbo:country dbr:France .

  ?pope rdf:type dbo:Pope .
  ?pope dbp:birthPlace ?birth_place .  # relation with the birth_place
}
LIMIT 50
```

----

Shortening sparql queries

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT * WHERE {
  ?s a foaf:Person ;
     dbp:birthPlace ?birth_place ;
     dbp:deathPlace ?death_place .
  ?birth_place dbo:country dbr:Italy .
  ?death_place dbo:country dbr:France .

  ?pope rdf:type dbo:Pope ;
        dbp:birthPlace ?birth_place .  # relation with the birth_place
}
LIMIT 50
```
