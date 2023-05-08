# Graph databases & SparQL

## Agenda

  - Storing and retrieving triples
  - Virtuoso
  - GraphDB

*Beware*: commands contain small typos. You must fix them to properly complete the course!

----

Prerequisites:

- json, yaml, xmlschema
- HTTP, OpenAPI 3
- SQL and database hints


---

## Graphs (again)

A graph is a set (unordered) of triples.

Each triple consists of a `subject`, `predicate`, `object`.

Graph databases such as [Virtuoso (opensource)](),
[GraphDB (proprietary)](),
[Amazon Nepture (proprietary SaaS)]()
support the [SparQL]() language.
Other databases - [Neo4j (opensource)]() use
custom language.

----

Let's populate some entries in SparQL
and see how it works.

Open [sample.ttl](sample.ttl) and list
all entries

```sparql
SELECT * WHERE {
  ?subject ?predicate ?object
}
```

(describe sparql query)

----

SparQL can then be used to correlate
entries using semantically defined
vocabularies such as FOAF.

```sparql
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .

SELECT * WHERE {
  ?s foaf:name ?o
}
```

| s | o |
| --- | --- |
| <mail:r@x.it> | "Roberto"|
| <mail:j@x.it> | "Jon"|

In this case `foaf:name` has a very specific meaning.
You don't need to create indexes in your database
to search for specific predicates.

----

Graph databases have an inference engine that can be used
to process complex queries.

```sparql
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .

SELECT * WHERE {
  ?s foaf:knows ?o 
```

| s | o |
| --- | --- |
| r@example | j@example |

----

And using multiple lines we can infer things
such as friend-of-a-friend emails.

```sparql
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .

SELECT DISTINCT ?mail1, ?mail3 WHERE {
  ?user1 foaf:knows ?user2
  . ?user2 foaf:knows ?user3

  . ?user1 foaf:mbox ?mail1  
  . ?user3 foaf:mbox ?mail3  
```

Note that the query describes each relation
ignoring the way data is stored.

---

# Querying DBPedia

[DBPedia](https://dbpedia.org/sparql) is a graph database with a lot of data inside.

We can use it to learn sparql.

- list concepts

```
select distinct ?Concept where {[] a ?Concept} LIMIT 20
```

----

Now we want to list all `Person`

```sparql
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

SELECT DISTINCT * WHERE {
  ?s a foaf:Person
} LIMIT 10
```

----

All `Person`s born in Pisa

```sparql

@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix dbr: <http://dbpedia.org/resource/> .

select distinct * where {
  ?s a foaf:Person .
  ?s dbp:birthPlace dbr:Pisa
} LIMIT 10

```

... with their deathplaces

```sparql
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .


select distinct * where {
?s a foaf:Person .
?s dbp:birthPlace dbr:Pisa .
?s dbp:deathPlace ?death_place
} LIMIT 10
```

----

If deathplace is in UK

```sparql

@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .

select distinct * where {
  ?s a foaf:Person .
  ?s dbp:birthPlace dbr:Rome .
  ?s dbp:deathPlace ?deathPlace .
  ?deathPlace dbo:country dbr:United_Kingdom
} LIMIT 50

```

----

We can extend the search to every person
born in Italy and dead in UK:

- replacing `dbr:Rome` with `?birth_place`
- restricting `?birth_place` to `dbr:Italy`

```sparql
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .

SELECT DISTINCT * WHERE {

?s a foaf:Person .
?s dbp:birthPlace ?birth_place .
?s dbp:deathPlace ?deathPlace .

?deathPlace dbo:country dbr:United_Kingdom .
?birth_place dbo:country dbr:Italy

} LIMIT 50
```

----

There's no limit to the inference, for example
we could require that the birthplace of that
person should match the one of a Pope.

```sparql
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

select distinct * where {
  ?s a foaf:Person .
  ?s dbp:birthPlace ?birth_place .
  ?birth_place dbo:country dbr:Italy .
  ?s dbp:deathPlace ?death_place .
  ?death_place dbo:country dbr:France .

  ?pope rdf:type dbo:Pope .
  ?pope dbp:birthPlace ?birth_place .  # relation with the birth_place
} LIMIT 50
```

----

Shortening sparql queries

```sparql
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbp: <http://dbpedia.org/property/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

select distinct * where {
  ?s a foaf:Person ;
     dbp:birthPlace ?birth_place ;
     dbp:deathPlace ?death_place .
  ?birth_place dbo:country dbr:Italy .
  ?death_place dbo:country dbr:France .

  ?pope rdf:type dbo:Pope ;
        dbp:birthPlace ?birth_place .  # relation with the birth_place
} LIMIT 50
```
