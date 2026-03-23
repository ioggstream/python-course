# OpenAPI & Modeling

## [OpenAPI](https://www.openapis.org/) is a specification language

OpenAPI is a specification language for REST APIs that allows to communicate:

- technical specifications

- metadata

- docs & references

## OpenAPI is driven by a [Foundation](https://www.openapis.org/)

The OpenAPI Foundation is an initiative under the Linux Foundation,
participated by government & companies  (gov.uk, Microsoft, Google, Oracle, IBM, ..):

- Driver for API adoption

- Evolution of Swagger 2.0

- Lightweight format: [YAML](https://learnxinyminutes.com/docs/yaml/)

- Generates docs & code via tools ([swagger-editor](https://editor.swagger.io), [apicur.io](https://www.apicur.io/))

- Allows reusable components via hyperlink (eg. $ref)

## OpenAPI Editor

Every OAS3 document begins with

```yaml
openapi: 3.0.0
```

Latest version is 3.2, and 4.0 is in the works.
This workshop is based on 3.0, but the most significant
changes in 3.1 and 4.0 are about the support of JSON Schema,
so they don't affect the basics of API modeling.

[Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/teamdigitale/api-starter-kit/master/openapi/simple.yaml.src) is a simple webapp for editing OpenAPI 3 language specs.

But there are a couple of tools that helps implementing interoperable APIs:

- [OAS Checker](https://italia.github.io/api-oas-checker/)
  is a tool to check if your OAS3 spec is compliant with the Italian API guidelines.

- [Schema Editor](https://teamdigitale.github.io/dati-semantic-schema-editor/) supports editing JSON Schema,
  with visual navigation.

## Start with Metadata

In OAS we start by describing api metadata, to clarify:

- API goals, audience and context;
- Terms of service;
- Versioning.

Here's a simple OAS3 metadata part, contained in the `info` section.

```yaml
openapi: 3.0.0
info:
  version: "1.0.0"
  title: |-
    Write a short, clear name of your service.
  description: |
    This field may contain the markdown documentation of the api,
    including references to other docs and examples.

  # Legal references and terms of services.
  termsOfService: 'http://swagger.io/terms/'
  contact:
    email: robipolli@gmail.com
    name: Roberto Polli
    url: https://github.com/ioggstream
  license:
    name: Apache 2.0
    url: 'http://www.apache.org/licenses/LICENSE-2.0.html'
```

## OpenAPI Metadata exercise


1. open [this incomplete OAS3 spec](https://editor.swagger.io/?url=https://raw.githubusercontent.com/ioggstream/python-course/main/connexion-101/notebooks/oas3/ex-01-info.yaml).

1. fix all errors and adding the missing fields: don't care for the specific detauls.

1. describe the first API we're going to implement: a service which returns the current
   timestamp in [RFC5454](https://tools.ietf.org/html/rfc5424#section-6.2.3)
   UTC (eg. `2019-01-01T00:00:00Z`).

1. provide contact informations and terms of services.

1. Feel free to add as many details as you want.

### Custom fields

Specific ecosystems may add custom fields to OAS spec, via the `x-` prefix.
This should be done with care, to avoid clashes between different ecosystems.

OAS3.1 defines the `summary` field, but in OAS3.0 you can use `x-summary` to provide a one-liner description for catalog purposes.

When publishing APIs, you may want to define lifecycle and sandboxing informations:
these could be done via custom fields like `x-lifecycle`

```yaml
  x-lifecycle:
    published: 1970-01-01
    deprecated: 2050-01-01
    retired: 2050-06-01
    maturity: published

```

**x-api-id** you may want to assign a time-persistend UUID to your API, so that you can change its `title`

```
x-api-id: 00000000-0000-0000-0000-000000000000
```

**x-gdpr** with a list of roles

**x-geodata** add local references in a machine readable format

## OpenAPI Metadata exercise: 2

```python
render_markdown(f'''

1- open [the previous OAS3 spec](/edit/notebooks/oas3/ex-01-info.yaml).

2- copy its content in the [Swagger Editor Online]({oas_editor_url('')}).

3- provide further informations via custom fields: if you think of any interesting
   label, define them and comment properly using `#`

''')
```
