# Agenda

- Enriching data with external knowledge

- Starting from a dataset, identify keywords that can be
  used to link entries to external knowledge.

## Graphs vs Tables

When we store data in tables,
whe have a fixed schema.

Constraints have advantages:

- performance;
- data integrity;
- consistency.

----

Column meaning is defined outside the table, or
where possible, in the table header.

When a row is associated with a specific entity,
the table has an identifier column,
usually indexed.

| id | name  | surname | spouse         |
|----|-------|---------|----------------|
| 1  | Homer | Simpson |  ... |
| 2  | Marge | Simpson |  ... |
| 3  | Bart  | Simpson |  ... |

Another database related to the same entity
may have a different schema.

| email              | name  | surname | parent         |
|--------------------|-------|---------|----------------|
| <homer@simpsons.com> | Homer | Simpson ||
| <marge@simpsons.com> | Marge | Simpson ||
| <bart@simpsons.com> | Bart  | Simpson |

With RDF, there is no fixed schema.
Instead, we have a public set of predicates
that can be used to describe the same entity.

```mermaid
graph LR

subgraph db1
 db1-id
 db1-name
 db1-surname
end

subgraph db2
 db2-email
 db2-name
 db2-surname
end

subgraph foaf
    givenName
    familyName
    mbox
    knows
end

db1-name --> givenName ~~~ db2-name --> givenName
db1-surname --> familyName ~~~ db2-surname --> familyName
db1-id --> mbox ~~~ db2-email --> mbox
```

Storing data in a graph allows to use
a set of predefined predicates (see them as properties)
that are globally defined.

---

Start with a json dataset.

```python

data = [
    {"email":"ft@a.test", "name": "Francisca", "surname": "Trujillo", "country": "ES"},
    {"email":"mr@a.test", "name": "Mario", "surname": "Rossi", "country": "IT"},
    {"email":"jd@a.test", "name": "Jane", "surname": "Doe", "country": "US"},
    {"email":"mg@a.test", "name": "Rashid", "surname": "Gowda", "country": "GB"},
]
```

Add a context to the dataset.

```python
context = {
        "@vocab": "https://schema.org/",
        "my": "https://a.test/my#",
        # The code property is appended to the base URL to form the country URI.
        "email": "@id",
        "@base": "<mailto:>",
        "name": "givenName",
        "surname": "familyName",
        # Define a custom country property.
        "country": "my:country",
    }
```

Now assemble everything in a JSON-LD graph

```python
nodes_ld = {
    # Every country is a resource.
    "@graph": data,
    "@context": context,
}
```

Exercise:

- add a `"@type": "Person"` to every entry

```python
nodes_ld = {
    # Every country is a resource.
    "@graph": [ { "@type": "Person", **c} for c in nodes],
    "@context": context,
}
```

And create a dataset and bind the selected namespaces.

```python
from rdflib import Dataset

d = Dataset(store='Oxigraph')
# Add ns shortcuts.
d.bind("eu", "https://publications.europa.eu/resource/authority/")
d.bind("schema": "https://schema.org/")
d.bind("euvoc": "http://publications.europa.eu/ontology/euvoc#")
d.bind("my":  "https://a.test/my#")

```

Exercise:

- list the graphs in the dataset; how many are there?

```python
import json
# Create a people graph and add the entries
d.graph(identifier="urn:People").parse(data=json.dumps(nodes_ld), format="application/ld+json")
```

Exercise:

- list the triples in the dataset;
- list the triples in the `urn:People` graph;

Load the countries vocabulary in a new graph.

```python
d.graph(identifier="eu:country").parse("countries-skos-ap-act.ttl", format="ox-turtle")
```

Now we have a graph to enrich with external data.

Match the custom country property with the ISO code
contained in the EU vocabulary
to retrieve the EU country identifier.

```python
q = """
SELECT DISTINCT
    ?person ?country
WHERE {

    # Match sentences in <urn:People>
    GRAPH <urn:People> {
        ?person
            a :Person ;
            my:country ?my_country_code .
    }

    # Match sentences in <eu:country>
    GRAPH <eu:country> {
        ?country a euvoc:Country ;
                skos:notation  ?isoCode ;
            .
    }

    # Match the isoCode of the country.
    FILTER ( ?isoCode = STRDT(?my_country_code,  euvoc:ISO_3166_1_ALPHA_2) )
}
"""

res = d.query(q)

[x.asdict() for x in res]

```

Exercise:

- Replace `<urn:People>` with `?g`: what happens?
- Can you replace both GRAPHs values with `?variables`?
- See the [string to datatype (STRDT) docs]

If that's OK, we can update the graph with the country identifier.

```python
q = """
INSERT {
  GRAPH <urn:People> {
    ?person :nationality ?country .
  }
}
WHERE {

    # Match sentences in <urn:People>
    GRAPH <urn:People> {
        ?person
            a :Person ;
            my:country ?my_country_code .
    }

    # Match sentences in <eu:country>
    GRAPH <eu:country> {
        ?country a euvoc:Country ;
                skos:notation  ?isoCode ;
            .
    }

    # Match the isoCode of the country.
    FILTER ( ?isoCode = STRDT(?my_country_code,  euvoc:ISO_3166_1_ALPHA_2) )
}
"""
d.update(q)
```

Now we can see the country identifier in the graph.

```python
print(d.graph(identifier="urn:People").serialize(format="turtle"))
```

Now, we can even have a "fat" graph with all the information

```python
q = """
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>
INSERT {
    GRAPH <urn:People> {
        ?p my:countryName ?countryName .
    }
}
WHERE {
    ?p a :Person ;
       :nationality ?country .

    ?country skos:prefLabel ?countryName .
    # We want the country name in English.
    FILTER ( LANG(?countryName) = "en" )
}
"""
d.update(q)

```

We can also mangle the data a bit...

```python
q = """
INSERT {
    GRAPH <urn:People> {
        ?p my:phone ?plus_prefix .
    }
}
WHERE {
    ?p a :Person ;
       :nationality _:country .

    _:country skos:notation ?prefix  .

    # We want the country name in English.
    FILTER ( DATATYPE(?prefix) = euvoc:PHONE_PREFIX )

    # Bind a modified value to the variable ?plus_prefix.
    BIND (
        CONCAT("+", str(?prefix)) AS ?plus_prefix
    )
}
"""
d.update(q)


```

Exercise:

- replace `?country` with `_:country`: does it work?
- replace the two sentences with the following **one**: does it work?

```raw
?p a :Person ;
   :nationality [
       skos:notation ?prefix
   ]
.
```
