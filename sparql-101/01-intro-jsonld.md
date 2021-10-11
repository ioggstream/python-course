# Modeling Semantic APIs

## Agenda

  - Semantics what?
  - Triples & co
  - Attaching semantics
  - Graph databases

*Beware*: commands contain small typos. You must fix them to properly complete the course!

----

Prerequisites:

- json, yaml, xmlschema
- HTTP, OpenAPI 3
- SQL and database hints

---


## Intro: Semantics what?

Semantics: the study of meaning.

Semantics ensures that a message is understood.

```
name: Mario Romildo
```

Is this a given name or a full name?

----

La mancanza di standardizzazione nel formato e significato dei dati ostacola l’interoperabilità tra le basi di dati di enti diversi e quindi la creazione di servizi digitali.

Un primo esempio è la mancanza di interoperabilità sintattica: una entità ben definita (eg. il codice fiscale) viene rappresentata con campi o formati diversi:

```
{"codice_fiscale": "MRORSS77T05E472W"}
{"cf": "mrorss77T05E472W"}
{"taxCode": "MRORSS77T05E472W"}
```

----

Un altro esempio è l'interoperabilità semantica: il concetto di famiglia ha diverse accezioni (eg. fiscale, anagrafica):

```
{"familiari": [
  {"nome": "Mario Rossi", "relazione": "padre"},
  {"nome": "Carla Rossi", "relazione": "sorella" , "convivente": false}   }

{"familiari": [
  {"nome": "Mario Rossi", "relazione": "padre"}
}
```

---

## Semantic standardization

Per standardizzare semanticamente i servizi e i loro contenuti, si utilizzano strumenti concettuali quali ontologie e vocabolari controllati (codelist, tassonomie, ..). 

Ontologia: una ontologia è un insieme di assiomi logici che concettualizzano un dominio di interesse definendo dei concetti e la semantica delle relazioni tra essi. Quando le ontologie contengono ulteriori restrizioni (eg. vincoli allo schema) non sono propriamente vocabolari.

----

Vocabolario controllato: un vocabolario dove i termini sono validati da un'autorità designata. Può essere di diversi tipi - eg. una lista (codelist), una struttura gerarchica (tassonomia), un glossario ed un tesauro (che aggiunge ad una tassonomia ulteriori vincoli). Esempi di vocabolari controllati europei si trovano qui https://op.europa.eu/en/web/eu-vocabularies/controlled-vocabularies

## Syntax standardization

Schema di dati: Uno schema è una rappresentazione/descrizione formale e machine-readable del contenuto effettivo o potenziale dei dati contenuti in un oggetto separato. In altre parole, è l'insieme di istruzioni semantiche e sequenziali che possono essere usate per controllare l'input memorizzato in un dato file, o per collegare un file che rispetta tali istruzioni a un sistema o un'applicazione di scambio di informazioni. Esistono diversi formati per descrivere degli schemi, tra cui xml-schema e json-schema. Definizione formale della sintassi di una entità. Vedi https://json-schema.org/understanding-json-schema/about.html

Un Vocabolario controllato supporta anche la standardizzazione sintattica.

----

Per standardizzare sintatticamente i servizi serve pubblicare degli schemi dati a cui tutte le organizzazioni devono conformarsi. Storicamente la standardizzazione degli schemi dati si basa sul concetto di namespace eventualmente distribuiti - vedi il formato di specifica XSD.

Se in ecosistemi ben definiti questo approccio funziona, al crescere della dimensione si pongono una serie di problematiche legate sia alla compattezza dei dati trasportati che del contesto di sicurezza legato ad esempio alla eventuale necessità di dereferenziare gli URI (eg. https://owasp.org/www-pdf-archive/XML_Based_Attacks_-_OWASP.pdf ) .

Mentre poi la metadatazione delle pagine tramite json-ld ha come platea principale i sistemi di processamento batch dei motori di ricerca, i dati convogliati tramite API vengono sempre più frequentemente processati da applicazioni mobile che hanno dei vincoli sia in termini di banda che di consumo di risorse (eg. batteria dei cellulari, riscaldamento) più stringenti.

Inoltre la creazione di servizi sempre più integrati porta ad un aumento del numero di richieste, e della conseguente necessità di supportare in maniera sostenibile i carichi sui sistemi IT.


---

## Defining semantic contents

I contenuti semantici vengono definiti
tramite proposizioni
`soggetto predicato complemento`
e loro insiemi (detti grafi)

Ecco un grafo con 3 proposizioni:

```
"il cane" "ha il colore" "nero"
"nero" "è" "un colore"
"il cane" "è" "un animale"
```

e una sua descrizione formale

```
prefix animals: <https://animals.example>
prefix colors: <https://animals.example>

animals:dog colors:hasColor colors:black
colors:black a colors:Color
animals:dog a animals:Animal
```

----

RDF: Resource Description Framework permette di rappresentare informazioni sul web basandosi su due strutture dati:

- **grafi** (insiemi di triple soggetto-predicato-oggetto);
- **elementi** (IRI, blank e literals);

e su dei **vocabolari** di elementi identificati tramite degli IRIs e dei namespace.

Un rdf-dataset è un insieme di **grafi**.

----


----

#### Ontologie

Per standardizzare la semantica dei contenuti
digitali si usano delle Ontologie.

In Italia esiste l'Ontologia delle persone
che possiamo usare per descrivere univocamente
qualcuno.

```
@prefix cpv: <https://w3id.org/italia/onto/CPV> .

<email:robipolli@gmail.com> cpv:givenName "Roberto" .
<email:robipolli@gmail.com> cpv:familyName "Polli" .

```

----

Anche l'ontologia è definita tramite triple
a partire da vocabolari di base.

```
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dct:   <http://purl.org/dc/terms/> .

https://w3id.org/italia/onto/CPV dct:modified  "2020-04-27"^^xsd:date ;
https://w3id.org/italia/onto/CPV dct:title     "Person Ontology"@en, "Ontologia delle persone"@it ;

```

---

### Json-LD

JSON-LD è un formato che permette di serializzare in JSON delle informazioni basate sul RDF data model.
 https://www.w3.org/TR/json-ld11/#data-model.

Un documento JSON-LD è quindi sia un documento RDF che JSON, e rappresenta un'istanza di un RDF data model.

JSON-LD inoltre *estende* RDF per permettere la serializzazione di dataset RDF generalizzati.
Di seguito l'estratto di sopra serializzato in JSON-LD/yaml.

```
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
molto usato sul web è www.schema.org. Le parole chiave
che definisce sono disponibili in formato json-ld
https://schema.org/docs/jsonldcontext.jsonld

---

È anche possibile ridefinire o localizzare i campi,
eventualmente usando diversi namespace.


```
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

```
-- come lista
occupation:
-  @value: "Student"
   @language: en
-  @value: "Etudiant"
   @language: fr
```

oppure

```
-- come oggetto
@context:
  occupation:
    @container: @language
occupation:
  en: Student
  fr: Etudiant
```

oppure

```
--- tramite elementi multipli, utile anche per la serializzazione di API semplici
@context:
  occupation: {@language: en}
  occupation_fr: {@language: fr}
occupation: Student
occupation_fr: Etudiant
```

---
### Json Schema e Json-LD

Per validare un oggetto json-ld, serve risolvere
ricorsivamente tutte le referenze:
è complesso farlo in maniera sincrona.

Quando si crea un API, la semantica va
definita in fase di specifica
in modo da non dover risolvere a runtime
referenze ricorsive
ed evitare problemi come il "@context mangling".

----

Un modo è associare un @context ad uno schema
integrandolo nella definizione attraverso
un valore `const`.
tramite un link
In questo caso, `pet` viene [disassociato dal vocabolario](https://w3c.github.io/json-ld-syntax/#example-25-using-the-null-keyword-to-ignore-data)

```
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

E' anche possibile indicare un link
```
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
O tramite `Link` header

```http
HTTP/1.1 200 OK
Content-Type: application/json
Link: <https://api.example/simple-person.jsonld>;
     rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"

{ "given_name": "Roberto", "family_name": "Polli" }
```

---

O tramite content-negotiation
ritornando più formati (json e json-ld)

```
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


## API e Semantica

Quando scambiamo informazioni tramite API
la semantica non è sempre chiara:

- è implicita;
- è in qualche pdf/xls;
- non è machine readable.

---
