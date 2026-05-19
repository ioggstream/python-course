# Reusing and bundling

Our strategy to standardize default responses, schemas and other components between
different API providers, is to provide those definitions in a shared and versioned file,
like <https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml>

API providers can then:

- `$ref`erence reusable components
- eventualy create a single bundled file containing all the resolved references (eg. with `openapi_resolver`)

With a set of common components API designers can create
better interfaces and ask themself questions like:

- am I considering enough error responses?
- can I reuse already existing schemas?
- should I implement a new schema for this object?

### Reusable components in OAS3

Supported reusable components can be:

- `schemas`: data types and objects
- `parameters`: request parameters, that may be defined in `headers`, `query` and `path`
- `responses`: http responses
- `securitySchemes`: security requirements to be applied to a given path

NOTE: in this course we won't go indeep on all the possibilities of OAS3, which you can see on the [OAS website](https://TODO)

### Exercise: replacing definitions with $refs

- Open this complete file [ex-05-01-bundle.yaml](ex-05-01-bundle.yaml)
- replace as many definitions as possible with references from the shared [definitions.yaml](https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml).


```python
# Exercise: create a bundle from the previous file with
!python -m openapi_resolver /code/notebooks/oas3/ex-05-01-bundle.yaml
```

### YAML anchors are your friends

YAML has a very nice feature, named **anchors**. They allow to define and reference
given portions of a YAML file.

```
# the following &anchor stores the `foo` value
a: &this_is_an_anchor foo

# *star dereferences the anchor
b: *this_is_an_anchor

```

See [anchors.yaml](/edit/notebooks/anchors.yaml)

```python
#  Check yaml file content.
from pathlib import Path

content = Path('anchors.yaml').read_text()

print(content)
```


```python
ret = yaml.safe_load(content)

assert ret['anchored_content'], ret['other_anchor']

print(ret['foo'])
print(ret['bar'])
```

    {'name': 'Everyone has same name', 'age': 10}
    {'name': 'Everyone has same name', 'age': 20}

### Using YAML anchors in OAS3

As every operation may have a set of predefined responses, namely:

- 503 Service Unavailable
- 429 Too Many Requests

You can put them in an `x-` custom parameter.which will be ignored by the OAS spec parser.

```
x-common-responses: &common-responses
  503ServiceUnavailable:
    $ref: ...
  429TooManyRequests:
    $ref: ...

```

Then use the `<<:` keyword and  `*anchor_name`  to reference them.

```
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

## NOTE: ANCHORS ARE PROCESSED BY THE YAML PARSER, NOT BY OAS

## OAS knows nothing about ANCHORS

```python

```
