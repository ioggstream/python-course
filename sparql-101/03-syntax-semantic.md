# Modeling Semantic APIs

## Agenda

- API e Semantica
- json-schema e json-ld

---

## API e Semantica

Quando scambiamo informazioni tramite API
la semantica non è sempre chiara:

- è implicita;
- è in qualche pdf/xls;
- non è machine readable.

Descrivendo un'API con un IDL (wsdl o OAS3)
possiamo descrivere la semantica includendola
nell'IDL.

---

### Semantica e Sintassi

La descrizione semantica di un'API
non abilita necessariamente delle comunicazioni
efficienti e sicure.

Per validare un oggetto json-ld, serve risolverne
ricorsivamente tutte le referenze:
è complesso farlo in maniera sincrona.

La possibilità di validare sintatticamente
i dati inoltre semplifica molto il quadro di interoperabilità.

Definendo inoltre la semantica va
definita in fase di specifica
evita di dover risolvere a runtime
referenze ricorsive
ed evita problemi di "@context mangling".

----

#### Collegare context e dati

Le specifiche json-ld definiscono un meccanismo per
per descrivere il contesto di un content json tramite `Link` header.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Link: <https://api.example/simple-person.jsonld>;
     rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"

{ "given_name": "Roberto", "family_name": "Polli" }
```

Ma non un meccanismo per associare queste informazioni ad uno schema.

----

#### Collegare context e schema

RDF non permette sempre di associare uno schema univoco agli
elementi di un grafo.

Anche associando una `Location` al luogo di nascita
di una persona tramite  `rdfs:range` con

```turtle
prefix cpv: <https://w3id.org/italia/onto/CPV/> .
prefix l0: <https://w3id.org/italia/onto/l0/> .

cpv:hasBirthPlace rdfs:range l0:Location
```

non è detto che sia semplice associare una sintassi
a `Location` che, in questo caso potrebbe essere ad esempio:

- un indirizzo
- una coppia di coordinate
- l'URI di un luogo

----

Uno scambio efficiente di informazioni in tempo reale
richiede una sintassi ben definita
validabile a runtime in modo efficiente.

La sintassi può essere validata con specifiche quali
[json-schema]() e [xmlschema]().

json-schema può essere usato anche per validare
la sintassi di un file json-ld.

----

Per dichiarare il @context associandolo ad uno schema
possiamo integrarlo nella definizione attraverso
un valore `const`.
Se una property è esterna al vocabolario,
basta
[disassociarla dal vocabolario](https://w3c.github.io/json-ld-syntax/#example-25-using-the-null-keyword-to-ignore-data)
assegnandole il valore `null`.

```yaml
# Associate a json-ld context to a schema
Customer:
  type: object
  required: [email]
  properties:
    "@context":
      const:
        "@vocab": "http://schema.org"
        pet: null
    email: {type: string}
    pet: {type: string}
```

----

E' anche possibile indicare un link,
evitando però di usarlo per poi alterare
la semantica dei dati.

```yaml
# Associate a json-ld context to a schema
Customer:
  type: object
  required: [email]
  properties:
    "@context":
      const: "https://api.example/customer-context.jsonld"
    email: {type: string}
    pet: {type: string}
```

----

Descrivendo un'API in formato OAS3 possiamo
descrivere i diversi formati usando i meccanismi
di content-negotiation.

```yaml
openapi: 3.0.1
...
paths:
  /users:
    get:
      ...
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Person"
            application/ld+json:
              schema:
                allOf:
                - type: object
                  properties:
                    "@context":
                      const:
                        "@vocab":   "https://w3id.org/italia/onto/CPV/"
                        given_name:  givenName
                        family_name: familyName
                - $ref: "#/components/schemas/Person"


```

---

### Vocabolario per la semantica

Un altro meccanismo per collegare @context
e schema, è quello di utilizzare un vocabolario
e delle parole chiavi all'interno dello schema.

Questo meccanismo è più semplice, ma richiede
di generare il @context a partire da un vocabolario esterno.

```yaml
Person:
  type: object
  properties:
    givenName:
      type: string
      x-refersTo: https://w3id.org/italia/onto/CPV/givenName
    familyName:
      x-refersTo: https://w3id.org/italia/onto/CPV/familyName
      type: string
  
```

### Ontologia per json-schema

Il progetto [Web of Things](https://w3.org/ns/td.jsonld) definisce invece
un vocabolario per "Thing description" in formato json-ld dove ad ogni property viene associato
sia un valore semantico che uno sintattico tramite il vocabolario
[json-schema](https://w3.org/ns/json-schema/).

