# Agenda

- Storing data vs Describing Knowledge
- JSON-LD

## Storing data

We store data in different ways and formats:
using constrained or loose schemas,
with more or less rigid serializations.

JSON (and YAML) is a human-readable way to
store data.

```yaml
[
  { name: Homer, surname: Simpson, spouse: Marge Simpson },
  { name: Marge, surname: Simpson, spouse: Homer Simpson },
]
```

We can then add identifiers (such as UUIDs or email), to be sure that cross references
are not ambiguous.

```yaml
[
  { email: homer@simpson.org, name: Homer, surname: Simpson, spouse: marge@simpson.org },
  { email: marge@simpson.org, name: Marge, surname: Simpson, spouse: homer@simpson.org },
]
```

Now we may have different datasets, such as the Springfield Elementary
school. Luckily we can "join" on an identifying field, but this is
not true for all fields.

```yaml
[
  { email: bart@simpson.org, name: Bart Simpson, parent: marge@simpson.org },
  { email: milhouse@vanhouten.org, name: Milhouse Van Houten, parent: kirk@vanhouten.org}
]
```

So we actually store data, but we lack knowledge.

### JSON-LD

JSON-LD is a JSON serialization for information described using the
[RDF data model](https://www.w3.org/TR/json-ld11/#data-model).

A JSON-LD document is both an RDF and a JSON document.

----

```python
homer = {
  "email": "homer@simpson.org",
  "name": "Homer",
  "surname": "Simpson",
  "spouse": "marge@simpson.org"
}
```

JSON-LD associates it with a context that disambiguates information

```python
import json

# A context maps JSON keys to IRIs.
context = {
  # Map name and surname to the IRI of the FOAF vocabulary.
  "name": "foaf:givenName",
  "surname": "foaf:familyName",
  # Use the email key as an IRI,
  #   prefixing it with the base IRI.
  "email": "@id",
  "@base": "https://simpsons.org#",
}
```

```python
homer_ld_json = json.dumps({
  "@context": context
  **homer
})
```

Exercise:

- load `homer_ld_json` in a Graph()
- print the serialization of the graph in `text/turtle` format


```python
from rdflib import Graph

```

<!-- g=Graph()-->
<!-- g.parse(data=homer_ld_json, format="application/ld+json")-->
<!-- print(g.serialize(format="text/turtle"))-->

---

<schema.org> is a collaborative vocabulary to
describe information about people, places, events, and more.
While it is not a formal ontology, and should be used with care
(e.g., in regulated domains),
it is widely used for search engine optimization (SEO) and
structured data markup, as well as for increase interoperability
in non-critical applications (e.g., e-commerce, marketing, ...).

Its terms are availabe here <https://schema.org/docs/jsonldcontext.jsonld>

---

Start with an object with fields in Italian:


```python
jane = {
  "nome": "Jane Doe",
  "nome_proprio": "Jane",
  "titolo": "Professor",
  "telefono": "(425) 123-4567"
}
```

Annotate it with schema.org.

```python
context = {
    "sdo": "https://schema.org/",
    "nome": "sdo:name",
    "nome_proprio": "sdo:givenName",
    "titolo": "sdo:jobTitle",
    "telefono": "sdo:telephone",
  }
```

```python
import json
jane_ld = {
  "@context": context,
  "@type": "sdo:Person",
  **jane
  }
print(json.dumps(jane_ld))
```

Exercise:

- load `jane_ld` in a Graph()
- what's the subject of the sentences?

```python
jane_ld_json = ...
```


---

### Localization

RDF (and JSON-LD) support localization natively.

```python
jane_ld["competenze"] =  {
    'it': 'Informatica',
    'en': 'Computer Science',
    'fr': 'Informatique'
}

# Associate the entry to the context.
jane_ld["@context"].update({
  "competenze" : {
    "@id": "sdo:skills",
    # The @container keyword
    #   does the magic of converting
    #   a dictionary into a list of objects.
    "@container": "@language"
  }
})
```

Now we can serialize the graph.

```python
from rdflib import Graph
g=Graph()
g.parse(data=json.dumps(jane_ld), format='json-ld')
print(g.serialize(format='turtle'))
```


Another localization mechanism allows
to map multiple values to a single property.

```python
jane_ld["soprannome"] = "Gianna"
jane_ld["soprannome_fr"] = "Jeanette"

# And the annotations.
jane_ld["@context"].update({
  "soprannome" : "sdo:alternateName",
  "soprannome_fr" : {
    "@id": "sdo:alternateName",
    "@language": "fr"
  }
})
```

---

#### Context mangling

Modifying a JSON-LD context,
alters the
meaning of the data.

Imagine you have a JSON-LD document
with a referenced context (i.e., a URL)
that is supposed to be downloaded
and used to interpret the data.

```yaml
"@context": https://payment/context.jsonld
payment_from: alice@foo.example
payment_to: bob@foo.example
```

Someone altering the <https://payment/context.jsonld>
could reverse the payment flow.

```yaml
# Original context
@context:
  payment_from: http://banking#debtor
  payment_to: http://banking#creditor
```

->

```yaml
# Altered context
@context:
  payment_to: http://banking#debtor
  payment_from: http://banking#creditor
```

----

When resolving contexts at runtime,
implementations should address these risks.
