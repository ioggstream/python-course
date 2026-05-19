# Schema registries and semantics with JSON-LD

## Bonus track: Semantic Extensions

> This section covers `x-jsonld-type` and `x-jsonld-context`,
> which align semantics across APIs without sharing the same schema.
> Full treatment is in the next lesson on JSON-LD.

----

### The problem: same field, different meaning

Two APIs may both have a `name` field, but mean different things:

- API A: `name` is a legal entity name (`schema:legalName`)
- API B: `name` is a display name (`foaf:name`)

Without semantic annotations, a consumer cannot distinguish them automatically.

----

### `x-jsonld-context` and `x-jsonld-type`

These OAS3 extension fields attach JSON-LD context to a schema,
making it machine-readable by semantic web tools.

```yaml
components:
  schemas:
    Organization:
      x-jsonld-type: 'https://schema.org/Organization'
      x-jsonld-context:
        '@vocab': 'https://schema.org/'
        name: 'legalName'
      type: object
      properties:
        name:
          type: string
          maxLength: 200
        vat_number:
          type: string
          pattern: '^[A-Z]{2}[0-9]{11}$'
```

----

### Why this matters

- APIs from different organizations can share data without sharing schemas.
- Tools like knowledge graphs and linked data processors can consume your API natively.
- The Italian API guidelines recommend this approach for public APIs exposing official data.

```python
# Exercise: add x-jsonld-type to the PersonResponse schema
# and point it to https://schema.org/Person
# Use this cell to sketch the YAML or test the annotation.
```

---
