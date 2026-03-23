# Mastering API Design at Scale

Welcome to Mastering API Design at Scale!
Author: <roberto.polli@par-tec.it>

---

## Agenda

- 15' Introducing OpenAPI, JSON Schema and service HTTP headers
- 15' Contract-First or Code-First?
- 15' API Canvas Design Methodology
- 15' Assisted API Design (with Spectral and validation tools)
- 15' Secure schema modeling

### Hints

- **Type in** exercises so you can learn from your mistakes
- If your notebook get stuck, **restart the kernel and run all** cells
- **Repetita iuvant**: concepts will be explained multiple times,
  from different perspectives, thoughout various notebooks.

## Teaser

In this course, we will learn how to design resilient APIs
using OpenAPI and JSON Schema in a contract-first approach.

```python
%pip install connexion[swagger-ui]
```

(and some validation tools)

```python
%pip install openapi-spec-validator
```

```python
%pip install jsonschema
```

The focus will be on API design, not on implementation,
since features can be implemented in different ways, both programmatically,
using frameworks or architectural compontents such as API gateways.

We will always start from an API Specification.

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: Person API
  version: 1.0.0
paths:
  /persons/{person_id}:
    get:
      parameters:
        - name: person_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: A person
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Person'
components:
  schemas:
    Person:
      type: object
      properties:
        name:
          type: string
        email:
          type: string
          format: email
```

Use a contract-first API framework to test the design...

for example [Connexion](https://connexion.readthedocs.io/en/latest/)

```bash
pip install connexion[swagger-ui]

connexion run --port 8080 --swagger-ui --watch openapi.yaml
```

... and contract-first tools to validate it, both statically
with Spectral


```bash
docker run --rm -v $(pwd):/app -w /app stoplight/spectral lint openapi.yaml
```

and dynamically with Schemathesis (that can be even integrated in pytest.)

```python
pip install schemathesis

schemathesis run openapi.yaml --checks all
```

We will also introduce JSON-LD and the concept of Semantic APIs
that allows referencing semantics to schemas,
to enable different API providers to align their APIs without
sharing the same schema.

```yaml
components:
  schemas:
    Person:
      x-jsonld-type: https://schema.org/Person
      x-jsonld-context:
        name: https://schema.org/givenName
        email: https://schema.org/email
      type: object
      properties:
        name:
          type: string
        email:
          type: string
          format: email
```
