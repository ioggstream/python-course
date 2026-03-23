# Reusing and bundling

Our strategy to standardize default responses, schemas and other components between
different API providers, is to provide those definitions in a shared and versioned file,
like https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml

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
# Exercise: creating a bundle from a $ref file
#
# You can resolve dependencies and create a bundle file with
!pip install openapi_resolver

```

    Requirement already satisfied: openapi_resolver in /usr/local/lib/python3.6/site-packages (0.0.5)
    Requirement already satisfied: pyyaml in /usr/local/lib/python3.6/site-packages (from openapi_resolver) (5.1.1)
    Requirement already satisfied: pathlib in /usr/local/lib/python3.6/site-packages (from openapi_resolver) (1.0.1)
    Requirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from openapi_resolver) (1.12.0)



```python
# Exercise: create a bundle from the previous file with
!python -m openapi_resolver /code/notebooks/oas3/ex-05-01-bundle.yaml
```

    openapi: 3.0.0
    info:
      title: foo
      version: '0.1'
    servers:
    - description: Development server
      url: https://localhost:8443/datetime/v1
    - description: Test server
      url: https://api.example.com/datetime/v1
      x-healthCheck:
        interval: 300
        timeout: 15
        url: https://api.example.com/datetime/v1/status
      x-sandbox: true
    paths:
      /echo:
        get:
          description: |
            Return the current timestamp, in the specified
            timezone. If the timezone does not
            exist returns 400 Bad Request, specifying that
            the given timezone is not in our database.
          operationId: api.get_echo
          parameters:
          - $ref: '#/components/parameters/tz'
          responses:
            503:
              $ref: '#/components/responses/503ServiceUnavailable'
            '200':
              content:
                application/problem+json:
                  example:
                    datetime: 20010507T00:00:10Z
                  schema:
                    $ref: '#/components/schemas/Datetime'
              description: |
                The current timestamp.
            '400':
              $ref: '#/components/responses/400BadRequest'
          summary: Return the current timestamp in RFC3339
      /status:
        get:
          description: |
            Ritorna lo stato dell'applicazione. A scopo
            di test, su base randomica puo' ritornare
            un errore.
          operationId: api.get_status
          responses:
            503:
              $ref: '#/components/responses/503ServiceUnavailable'
            '200':
              content:
                application/problem+json:
                  example:
                    detail: The app is running smoothly.
                    status: 200
                    title: OK
                  schema:
                    $ref: '#/components/schemas/Problem'
              description: |
                Il server ha ritornato lo status. In caso di problemi
                ritorna sempre un problem+json.
          summary: Ritorna lo stato dell'applicazione.
    components:
      headers:
        Retry-After:
          description: |-
            Retry contacting the endpoint *at least* after seconds.
            See https://tools.ietf.org/html/rfc7231#section-7.1.3
          schema:
            format: int32
            type: integer
      parameters:
        tz:
          in: query
          name: tz
          schema:
            $ref: '#/components/schemas/Timezone'
      responses:
        400BadRequest:
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/Problem'
          description: Bad Request
        503ServiceUnavailable:
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/Problem'
          description: Service Unavailable
          headers:
            Retry-After:
              $ref: '#/components/headers/Retry-After'
      schemas:
        Datetime:
          properties:
            timestamp:
              example: 2019-01-01 00:00:00
              format: datetime
              type: string
          required:
          - timestamp
        Problem:
          properties:
            detail:
              description: |
                A human readable explanation specific to this occurrence of the
                problem. You MUST NOT expose internal informations, personal
                data or implementation details through this field.
              example: Request took too long to complete.
              type: string
            instance:
              description: |
                An absolute URI that identifies the specific occurrence of the problem.
                It may or may not yield further information if dereferenced.
              format: uri
              type: string
            status:
              description: |
                The HTTP status code generated by the origin server for this occurrence
                of the problem.
              example: 503
              exclusiveMaximum: true
              format: int32
              maximum: 600
              minimum: 100
              type: integer
            title:
              description: |
                A short, summary of the problem type. Written in english and readable
                for engineers (usually not suited for non technical stakeholders and
                not localized); example: Service Unavailable
              type: string
            type:
              default: about:blank
              description: |
                An absolute URI that identifies the problem type.  When dereferenced,
                it SHOULD provide human-readable documentation for the problem type
                (e.g., using HTML).
              example: https://tools.ietf.org/html/rfc7231#section-6.6.4
              format: uri
              type: string
          type: object
        Timezone:
          description: |
            A timezone in the form of continent/city
            or "UTC".
          example: Europe/Rome
          type: string


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

    #
    # YAML examples from https://learnxinyminutes.com/docs/yaml/
    #

    anchored_content: &anchor_name This string will appear as the value of two keys.
    other_anchor: *anchor_name

    # Anchors can be used to duplicate/inherit properties
    base: &base
      name: Everyone has same name

    # The regexp << is called Merge Key Language-Independent Type. It is used to
    # indicate that all the keys of one or more specified maps should be inserted
    # into the current map.

    foo: &foo
      <<: *base
      age: 10

    bar: &bar
      <<: *base
      age: 20





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

Then use the `<<: ` keyword and  `*anchor_name`  to reference them.

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
