# Knowledge Management 101

## Agenda

- Knowledge management
- Semantics what?
- Triples & co
- Attaching semantics
- Graph databases
- JsonLD

*Beware*: commands may contain small typos. You have to fix them to properly complete the course!

----

## Intro: Semantics what?

Semantics: the study of meaning.

Semantics ensures that a message is understood;
messages include data and HTTP exchanges.

Here are some ambiguous messages:

```yaml
name: FABIANO Romildo
income: 4_000_000
```

Is this a given name or a full name?
What is the currency of the income?
Is it a monthly or yearly income?

----

Integrating data from different sources is difficult because of the lack of semantic interoperability.

```mermaid
graph LR
Am>"{name: FABIANO Romildo\nincome: 4_000_000}"]
Cm>"{givenName: FABIANO\nfamilyName: Romildo\ntax: 12_000EUR}"]
B((Data sink))

A((Data source 1)) ---Am --> B
C((Data source 3)) ---Cm --> B
```

----

Identifiers may differ between systems,
and even registry data are not always interoperable.

```mermaid
graph LR
Am>"{givenName: Angela\nfamilyName: Merkel\ndate_of_birth: 1954-07-17}"]
Cm>"{givenName: Angela\nfamilyName: Kasner\ndate_of_birth: 1954-07-17}"]
B((Data sink))

A((Data source 1)) ---Am --> B
C((Data source 3)) ---Cm --> B
```

----

The lack of standardization in the format and meaning of data
hinders interoperability between the databases of different organizations,
and even inside different branches of the same organization,
and therefore the creation of digital services.

A first example is the lack of syntactic interoperability:
a well-defined entity (eg. the tax code) is represented with different fields or formats:

```
{"tax_code": "MRORSS77T05E472W"}
{"cf": "mrorss77T05E472W"}
{"taxCode": "MRORSS77T05E472W"}
```

----

Another example is semantic interoperability: the concept of family has different meanings (eg. in the fiscal domain, in the registry domain, ..):

```yaml
relatives:
  - name: Mario Rossi
    relationship: father
  - name: Carla Rossi
    relationship: sister
    cohabiting: false
```

```yaml
relatives:
  - name: Mario Rossi
    relationship: padre
```

---

## Vocabularies to the rescue

Controlled Vocabularies use URIs to disambiguate the meaning of terms and provide semantics.

Every term is identified by an absolute URI.
The prefix identifies the vocabulary name,
and the suffix identifies the term.

```python

dog_uri = "https://dbpedia.org/data/Dog"

```

To semantically standardize data, services and their content, conceptual tools such as ontologies and controlled vocabularies (codelist, taxonomies, ..) are used.

Ontology: an ontology is a set of logical axioms that conceptualize a domain of interest by defining concepts and the semantics of relationships between them.

When ontologies contain further restrictions (e.g.,

Controlled vocabulary: a vocabulary where the terms are validated by a designated authority.
It can be of different types - EG.A list (codelist), a hierarchical structure (taxonomy), a glossary and a tesauro (which adds further constraints to a taxonomy).

Examples of European controlled vocabularies are found here <https://op.europa.eu/en/web/eu-vocabularies/controlled-vocabularies>

## Syntax standardization

Data model: a data model, or data schema is a formal representation/description and machine-readable of the actual or potential content of the data contained in a separate object.

In other words, it is the set of semantic and sequential instructions that can be used
to check the stored input in a given file,
or to connect a file that respects these instructions to a system or an application of exchange of information.

There are several formats to describe the patterns,
including XML Schema  and JSON Schema. Formal definition of the syntax of an entity.
See <https://json-schema.org/understanding-json-schema/about.html>

A Controlled vocabulary may support syntactic standardization.

----

To syntactically standardize the services, you need to publish data patterns to which all organizations must conform.Historically, the standardization of the data schemes is based on the concept of Namespace possibly distributed - see the XSD specification format.

If in well-defined ecosystems this approach works, as the dimension grows, a series of problems related to both the compactness of the transported data and the security context linked for example to the possible need to dereference the URI (Eg. <Https://owasp.org/www-pdf-rchive/xml_based_attacks_-_owasp.pdf>) are

While then the metadation of the pages via Json -ild has as its main audience the search engines batch processing systems, the data conveyed through APIs are increasingly frequently processed by mobile applications that have constraints both in terms of bandwidth and consumption of resources (eg. Cellular battery, heating) more stringent.

In addition, the creation of increasingly integrated services leads to an increase in the number of requests, and the consequent need to sustain the loads on IT systems in a sustainable way.
---

## Defining semantic contents

Semantic contents are defined through
sentences of the form
`subject predicate object`
and their sets (called graphs).

Here is an example of a graph with three sentences:

```
"the dog" "has the color" "black"
"the dog" "is an" "animal"
"black" "is a" "color"
```

and an associated formal description in text/turle

```
prefix animals: <https://animals.example>
prefix colors: <https://animals.example>

animals:dog colors:hasColor colors:black
colors:black a colors:Color
animals:dog a animals:Animal
```

----

RDF: Resource Description Framework

allows to represent information on the web based on two data structures:

- **elements** (IRIs, blank nodes and literals);
- **triples** (subject-predicate-object);
- **graphs** (sets of triples).

and on **vocabularies** of elements identified by IRIs and namespaces.

An RDF dataset is a set of **graphs**.

----

#### Ontologies

To standardize the semantics of digital content,
we use ontologies.

In Italy, there's the official ontology of person
(Common Person Vocabulary) that we can use to uniquely describe someone.

```
@prefix cpv: <https://w3id.org/italia/onto/CPV> .

<email:robipolli@gmail.com> cpv:givenName "Roberto" .
<email:robipolli@gmail.com> cpv:familyName "Polli" .

```

----

An ontology is defined by a set of IRIs and their relationships.

```
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dct:   <http://purl.org/dc/terms/> .

https://w3id.org/italia/onto/CPV dct:modified  "2020-04-27"^^xsd:date ;
https://w3id.org/italia/onto/CPV dct:title     "Person Ontology"@en,
                                               "Ontologia delle persone"@it ;

```

---

### Json-LD

JSON-LD è un formato che permette di serializzare in JSON delle informazioni basate sul
[RDF data model](https://www.w3.org/TR/json-ld11/#data-model).

Un documento JSON-LD è quindi sia un documento RDF che JSON, e rappresenta un'istanza di un RDF data model.

JSON-LD inoltre *estende* RDF per permettere la serializzazione di dataset RDF generalizzati.

----
Dato un oggetto JSON

```yaml
id: robipolli@gmail.com
given_name: Roberto
family_name: Polli
```

JSON-LD permette di trasformarlo in un grafo RDF associandogli un contesto.

```yaml
"@context":
  cpv: "https://w3id.org/italia/onto/CPV"
  given_name: "cpv:givenName"
  family_name: "cpv:familyName"
  id: "@id"
id: robipolli@gmail.com
given_name: Roberto
family_name: Polli
```

---

Oltre all'ontologia italiana, un altro vocabolario
molto usato sul web è <www.schema.org>. Le parole chiave
che definisce sono disponibili in formato json-ld
<https://schema.org/docs/jsonldcontext.jsonld>

---

È anche possibile ridefinire o localizzare i campi,
eventualmente usando diversi namespace.

```yaml
"@context":
  "sdo": "http://schema.org/"
  "nome":"sdo:name"
  "nome_proprio": "sdo:givenName"
"@type": "Person"
  "nome": "Jane Doe"
  "nome_proprio": "Jane"
  "sdo:jobTitle": "Professor"
  "sdo:telephone": "(425) 123-4567"
```

---

### Localizzazione

JSON-LD supporta nativamente informazioni
localizzate:

```yaml
-- come lista
occupation:
-  @value: "Student"
   @language: en
-  @value: "Etudiant"
   @language: fr
```

oppure

```yaml
-- come oggetto
@context:
  occupation:
    @container: @language
occupation:
  en: Student
  fr: Etudiant
```

oppure

```yaml
--- tramite elementi multipli, utile anche per la serializzazione di API semplici
@context:
  occupation: {@language: en}
  occupation_fr: {@language: fr}
occupation: Student
occupation_fr: Etudiant
```

---

#### Context mangling

@context mangling: modificando il contesto di un oggetto
se ne altera il significato.

```yaml
payment_from: alice@foo.example
payment_to: bob@foo.example
"@context": https://payment/context.jsonld
```

Alterando la risposta del server <https://payment/context.jsonld>
possiamo invertire il verso del pagamento!

```yaml
@context:
  payment_from: http://banking#debtor
  payment_to: http://banking#creditor
```

->

```yaml
@context:
  payment_to: http://banking#debtor
  payment_from: http://banking#creditor
```

----

Esistono diverse ipotesi tecnologiche basate
sull'elaborazione semantica dei dati a runtime.
Tutte queste implementazioni devono indirizzare
questo tipo di rischi.
