# Secure Schema Design

In an API ecosystem, schemas are one of the building blocks of interoperability.
They:

- define the syntax of exchanged data;
- may define the semantics (aka the meaning) of the data.

Schemas should be:

- safe (e.g., prevent injection attacks);
- evolvable (e.g., allow adding new fields without breaking clients);
- consistent (e.g., use the same field names and formats across APIs).

----

To avoid schema proliferation, use:

- catalogs;
- guidelines based on common specifications.

---

## Agenda

- Schemas: definition, reuse, and `$ref`
- Generating schemas: `datamodel-code-generator`
- Request schemas: validating untrusted input
- Response schemas: stable and flexible contracts
- Problem Details: standardized error modeling
- Security aspects: preventing injection and enforcing constraints
- Validating schemas with OAS Checker
- Bonus track: semantic extensions - `x-jsonld-type` and `x-jsonld-context`

---

Prerequisites:

- OpenAPI 3 basics
- JSON Schema types: `string`, `integer`, `object`, `array`

---

## Schemas

OAS allows defining, using and reusing schemas.

A schema describes what data looks like
(the syntax): its fields, types, and constraints.

While OAS allows defining schemas inline,
the best practice is to define them in the `#/components/schemas` section and reference them with `$ref`.
This promotes reuse and consistency.

----

### Reusable schemas

OAS schemas must be embedded in the `#/components/schemas` section
of an OAS document.
Schemas outside OAS documents must be defined as JSON Schema files,
with all the proper headings and metadata.

:warning: A schema used for request or response,
should always be a JSON object, even if it has only one field.
This allows adding new fields in the future without breaking clients
and provides a consistent structure for all requests and responses.

----

:warning: If your API ecosystem relies on OAS,
embedding all schemas in OAS is a sensible choice.

```yaml
openapi: 3.0.0
...
components:
  schemas:
    Person:
      description: |-
        A person object represents an individual
        with a name, identified by a tax code.
      type: object
      required: [tax_code, given_name, family_name]
      properties:
        tax_code:
          type: string
          pattern: '^[A-Z0-9]{16}$'
        given_name:
          type: string
          maxLength: 200
        family_name:
          type: string
          maxLength: 200
```

----

You can publish it on the web (e.g. GitHub Pages) and reference it from other specs with `$ref`:

```yaml
...
schema:
  $ref: '#/components/schemas/Person'
```

----

### Infrastructural components schemas

OAS allows defining schemas for both domain entities (e.g. `Person`) and infrastructural components(e.g. `Problem`, `Pagination`, `ThrottlingHeaders`).

----

For example

In your ecosystem, you should have a curated registry of common schemas
for infrastructural components (e.g. `Problem`, `Pagination`, `ThrottlingHeaders`).
All APIs can reference them via `$ref` to ensure consistency.

----

### Referencing external schemas

The `$ref` value is an URI.

```yaml
components:
  schemas:
    Problem:
      $ref: 'components.oas3.yaml#/components/schemas/Problem'
```

> Note: Schema registries guarantee consistency: if a shared schema adds a required field,
> all APIs referencing it will pick up the change.

For this reason, it's important that:

- publishers version their schemas (e.g. `0.0.5` in the example above) to avoid breaking changes;
- consumers reference a specific version to ensure stability and assemble the final API contract before distributing it (see the bundling section).

:warning: In OAS3.1 and JSON Schema, $refs may just be "identifiers"
and not downloadable URLs: you may need to use a specific resolver for them.

----

### Generating code from schemas

You can generate Pydantic models from an OAS3 spec
from a [Terminal](/terminal/) with `datamodel-code-generator`:

```python
!pip install datamodel-code-generator
datamodel-codegen \
  --input notePersons/oas3/store.yaml \
  --input-file-type openapi \
  --output generated_model.py
```

```python
# Inspect the generated models.
```

If your schemas have further requirements,
you may extend the generated models with custom code
without modifying the generated file (e.g. `generated_model.py`).

---

## Request Schemas

A request schema describes untrusted input - data coming from the outside world.
Treat it with suspicion: validate strictly, reject unexpected fields.

Key rules for request schemas:

- Always add `example` values to clarify the expected format,
  and beware that users tend to trust examples more than descriptions or specifications.
- Always specify `required` fields - never assume a field is present.
- Use `maxLength` on strings to prevent oversized payloads.
- Set `additionalProperties: false` to reject unknown fields.
- Use `pattern` or `format` to constrain string shapes (e.g. `date`, `uuid`).
- Avoid `default` values that hide missing data - fail early instead.
- Consider `writeOnly/readOnly` to reuse schemas for both requests and responses while enforcing field visibility.

----

### Example: strict request schema

By default, OAS (and JSON Schema) allows extra fields
that are not defined in the schema.
This can lead to security issues and data pollution if not handled properly.

```yaml
components:
  schemas:
    PersonRequest:
      type: object
      additionalProperties: false   # explicitly reject unexpected fields
      required: [given_name, family_name]
      properties:
        given_name:
          type: string
          minLength: 1
          maxLength: 64
          example: "Mario Valerio"
        family_name:
          type: string
          minLength: 1
          maxLength: 64
        tax_code:
          type: string
          pattern: '^[A-Z0-9]{13}$'
```

----

### Why `additionalProperties: false` matters

Without it, a client can send extra fields that may:

- bypass business logic validation
- pollute your data store with unexpected keys
- expose internal field names via trial-and-error

----

### Exercise: write a strict request schema

Exercise: write a `Person` schema to be used in
a request.

- `given_name` and `family_name` are required, with a max length of 64 characters.
- `given_name` and `family_name` should accept only
  latin unicode characters
  (hint, use the following regex pattern:
  to match latin unicode letters
  `[A-Za-z\u00C0-\u024F ]`)
- `tax_code` is required.

Reject any extra fields.

```yaml
# Complete the schema below.
components:
  schemas:
    Person:
      type: object
      additionalProperties: ...
      required: [...]
      properties:
        tax_code:
          type: string
        ...
```

---

## Response Schemas

A response schema describes your output data.
Here the goal shifts from security to stability and evolvability.
While the model can be more flexible, you may want to ensure
that your system generates the expected structures.

----

:warning: Your API architecture may be configured
to enforce response schemas at runtime: this avoids
accidental publication of extra fields
or errored response.

----

Some hints:

- Don't remove required fields in new versions - that is a breaking change.
- Mark read-only fields with `readOnly: true` (e.g. `id`, `created_at`).

----

Annotate fields with `readOnly` and `writeOnly`
to control their visibility in requests and responses.

This allows reusing the same schema for both
requests and responses,
while ensuring that certain fields (even required ones)
are only present in one direction.

----

### Example: flexible response schema

```yaml
components:
  schemas:
    Person:
      type: object
      required: [tax_code, given_name, family_name, created_at]
      properties:
        ...
        created_at:
          type: string
          format: date-time
          example: '2024-01-01T12:00:00Z'
          readOnly: true  # this field is only present in responses, not in requests

```

#### Null fields in OAS and JSON Schema

OAS3 allows you to set `nullable: true` on any field
but does not have a `null` type.
JSON Schema allows setting `type: ["string", "null"]` to allow null values.

```yaml
openapi: 3.0.0
components:
  schemas:
    NullableString:
      type: string
      nullable: true
```
----

JSON Schema is more flexible but implementing tools may require tweaks.

```yaml
# 2020-12
$schema: https://json-schema.org/draft/2020-12/schema
NullableString:
  type:
  - "string"
  - "null"
NullableString2:
  anyOf:
  - type: string
  - type: "null"
```

---

## Problem Details

When something goes wrong, clients need a consistent error format.
[RFC9457](https://www.rfc-editor.org/rfc/rfc9457) defines Problem Details,
a standard JSON structure for HTTP error responses.

```json
{
  "type": "https://example.com/errors/out-of-stock",
  "title": "Out of Stock",
  "status": 503,
  "detail": "Product XYZ is currently unavailable.",
  "instance": "/orders/123"
}
```

----

### Using Problem Details in OAS3

Define a basic `Problem` schema in your registry:
you may want to constrain string lengths and patterns
to ensure consistent errors
(e.g., `type` should be a URI matching [A-Z0-9_-/:]{1,256}).

```yaml
components:
  schemas:
    Problem:
      $ref: 'components.oas3.yaml#/components/schemas/Problem'
```

----

Then use it for all error responses, including `default`:

```yaml
paths:
  /Persons/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PersonResponse'
        'default':
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/Problem'
```

----

## Security Aspects

Schema design is your first line of defense against injection attacks and data leaks.

OAS-aware API Gateways may enforce schema constraints at runtime:
this is great to block malicious payloads before they reach your application.

### Preventing injection attacks

- Always validate `format`: a field typed as `date` should reject `2024-01-01'; DROP TABLE orders;--`.
- Use `pattern` for identifiers and codes: `^[a-zA-Z0-9_-]{1,64}$`.
- Set `maxLength` on every string field - unbounded strings enable DoS and buffer issues.
- Never echo back raw input in error messages - use Problem Details with a generic `detail`.

----

### Sensitive fields

- Mark fields that must never appear in responses with `writeOnly: true` (e.g. passwords).
- Mark fields that must never appear in requests with `readOnly: true` (e.g. `id`, server timestamps).

```yaml
properties:
  password:
    type: string
    writeOnly: true
    minLength: 12
    maxLength: 128
  id:
    type: string
    format: uuid
    readOnly: true
```

----

### Avoiding data leaks in errors

:warning: Never include stack traces, SQL errors, or internal paths in API responses.
Problem Details lets you decouple the user-facing `detail` from your internal logs:

```python
import logging

def get_Person(Person_id):
    try:
        return db.find(Person_id)
    except Exception as e:
        logging.exception("DB error fetching Person %s", Person_id)
        return {"type": "about:blank", "title": "Internal Error", "status": 500}, 500
```

Proper Problem Details implementations may even provide an additional line of defence
by redacting responses before they are sent to clients.

---

## Validating with OAS Checker

[OAS Checker](https://italia.github.io/api-oas-checker/) validates your spec
against the Italian API guidelines, which include security rules like:

- All string fields must have `maxLength`.
- All numeric fields should have `minimum`/`maximum`.
- Error responses must use `application/problem+json`.
- `$ref` to well-known schemas (Problem, throttling headers) is recommended.

It is based on Spectral: this means that you can
integrate the published rulesets in your CI/CD pipeline
just adding them to your Spectral/Super-Linter configuration.

----

### Running OAS Checker Online

Try the [online editor](https://italia.github.io/api-oas-checker/) - paste your YAML
and review the rule violations on the right panel.

----

### Schema Editor

[Schema Editor](https://teamdigitale.github.io/dati-semantic-schema-editor/) provides
a visual interface to:

- Navigate nested schema properties
- Add and edit fields with a form UI
- Export the schema back to JSON Schema or OAS3 YAML

Use it when modeling complex nested objects - it is easier than editing YAML by hand.

---

## Exercise

Edit [ex-03-02-path.yaml](/edit/notebooks/Persons/oas3/ex-03-02-path.yaml) so that:

1. every `/status` response uses the `Problem` schema;
2. the `components/schemas` section defines `Problem` via `$ref` to the external registry;
3. both the `200` and `default` responses use `application/problem+json`.

Look at [ex-03-02-path-ok.yaml](/edit/notebooks/Persons/oas3/ex-03-02-path-ok.yaml) for the solution.

----

### Test the exercise

Start the connexion app pointing at your edited spec, then run the cell below.

```python
import requests

BASE_URL = "http://localhost:5000"

resp = requests.get(f"{BASE_URL}/status")
print(resp.status_code, resp.headers.get("Content-Type"))
print(resp.json())
```

```python
# Verify the response follows the Problem Details structure.
data = resp.json()
assert "status" in data, "Missing 'status' field"
assert "title" in data, "Missing 'title' field"
print("OK - response matches Problem Details schema")
```

---
