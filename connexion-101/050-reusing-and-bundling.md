# Reusing and bundling

To standardize default responses,
schemas and other components between
different API providers,
publish definitions in a shared and versioned file
(e.g., [components.oas3.yaml](/edit/notebooks/oas3/components.oas3.yaml)).

----

API providers can then:

- `$ref`erence reusable components
- eventualy create a single bundled file containing all the resolved references (eg. with `openapi_resolver`)

----

With a set of common components API designers can create
better interfaces and ask themself questions like:

- am I considering enough error responses?
- can I reuse already existing schemas?
- should I implement a new schema for this object?

---

## Reusable components in OAS3

Supported reusable components can be:

- `schemas`: data types and objects
- `parameters`: request parameters, that may be defined in `headers`, `query` and `path`
- `responses`: http responses
- `securitySchemes`: security requirements to be applied to a given path

NOTE: this course doesn't cover on all the possibilities of OAS3.
See the [OAS website](https://github.com/OAI/OpenAPI-Specification).

----

### Exercise: replacing definitions with $refs

- Open [ex-05-01-bundle.yaml](/edit/notebooks/oas3/ex-05-01-bundle.yaml)
- replace as many definitions as possible with references from the shared
<https://raw.githubusercontent.com/ioggstream/python-course/refs/tags/v2026.05.1/connexion-101/notebooks/oas3/components.oas3.yaml>
- "resolve" the OAS file as JSON.

```python
import yaml, json
d = yaml.safe_load(stream=open("oas3/ex-05-01-bundle-ok.yaml"))
json.dump(d, open("deleteme.json", "w+"))
```

----

### Exercise: create a bundle from the previous file

If you have docker, you can use the Redocly CLI to create a bundle from the previous file.

A bundle is a single file containing all the resolved references. It can be used to share your API definition with others, or to deploy it to a server.

```bash
# Exercise: create a bundle from the previous file with
docker run --rm -v $PWD:/app
docker.io/redocly/cli@sha256:78fa111b6c84522383d419a0631c984aefa76c5fbd39d8904a201b86e3b44168 /app/oas3/ex-05-01-bundle-ok.yaml bundle --output /app/deleteme.yaml
```

---

## YAML as a template engine

YAML can be used as a template engine for your OAS files. It allows you to define reusable components and reference them in your OAS file.

```mermaid
graph TD

YAML[YAML OAS source]
-->|processing| JSON[JSON OAS with $refs]
-->|bundling| --> BUNDLE[OAS with resolved $refs]
```

----

YAML has a nice feature, named **anchors**. They allow to define and reference
given portions of a YAML file.

```yaml
# the following &anchor stores the `foo` value
a: &this_is_an_anchor foo

# *star dereferences the anchor
b: *this_is_an_anchor
```

----

See [anchors.yaml](/edit/notebooks/anchors.yaml)

```python
#  Check yaml file content.
from pathlib import Path
import yaml

content = Path('anchors.yaml').read_text()

print(content)
```

----

Check anchor content:

```python
ret = yaml.safe_load(content)

assert ret['anchored_content'], ret['other_anchor']

print(ret['foo'])
print(ret['bar'])
```

----

### Using YAML anchors in OAS3

If you have a set of constants in your API definition
e.g., maximum number of items in a list, or common responses, you can use YAML anchors to define them once and reuse them everywhere.

```yaml
openapi: 3.0.0
...
components:
  schemas:
    MaxItems:
      type: integer
      maximum: &max-items 100
    Limit:
      type: integer
      maximum: *max-items  # Reuses the max-items anchor
...
```

----

### YAML merge keys

Merge keys are a special feature of YAML that allows you to merge
 the content of one or more dicts.
 This can be useful when you have a set of common properties that you want to reuse across multiple objects.

:warning: YAML merge keys are not supported by all YAML parsers, and they are not part of the OAS specification. While they are widely used on the web, they are formally deprecated in YAML 1.2.
Nonetheles, I find them very useful to avoid using a specific template engine to generate OAS files and manage safely model composition without recurring to `allOf` and `oneOf` keywords, which might cause nesting and readability issues.



As every operation may have a set of predefined responses, namely:

- 503 Service Unavailable
- 429 Too Many Requests

You can put them in an `x-` custom parameter.which will be ignored by the OAS spec parser.

```yaml
x-common-responses: &common-responses
  503ServiceUnavailable:
    $ref: ...
  429TooManyRequests:
    $ref: ...

```

----

Then use the `<<:` keyword and  `*anchor_name`  to reference them.

```yaml
paths:
  /status:
    get:
      ...
      responses:
        # Add the anchored responses
        <<: *common-responses

        # And now the other ones.
        '200':
          ...
```

:warning: ANCHORS ARE PROCESSED BY THE YAML PARSER, NOT BY OAS
:warning: OAS knows nothing about ANCHORS

For YAML interoperability considerations
see <https://www.rfc-editor.org/rfc/rfc9512.html>.
