# OpenAPI & Modeling

[OpenAPI](https://www.openapis.org/) is a specification language
for REST APIs that documents:

- technical specifications
- metadata
- docs & references

----

OpenAPI is driven by a [Foundation](https://www.openapis.org/)
under the Linux Foundation,
participated by government & companies
(gov.uk, Microsoft, Google, Oracle, IBM, ..):

- Driver for API adoption
- Evolution of Swagger 2.0
- Lightweight format: YAML or JSON
- Generates docs & code via tools (e.g., [swagger-editor](https://editor.swagger.io))
- Allows reusable components via hyperlink (eg. `$ref`)

----

Latest version is 3.2, and there's work ongoing on the 4.0.
This workshop is based on 3.0, but the most significant
changes in 3.1 and 4.0 are about the support of JSON Schema,
so they don't affect the basics of API modeling.


## OpenAPI Editor

Every OAS3 document begins with

```yaml
openapi: 3.0.0
```

[Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/teamdigitale/api-starter-kit/master/openapi/simple.yaml.src) is a simple webapp for editing OpenAPI 3 language specs.

The Italian Govenment built a couple of tools that help implementing interoperable APIs
(disclaimer: I authored the tools when I worked there):

- [OAS Checker](https://italia.github.io/api-oas-checker/)
  is a tool to check if your OAS3 respects the Italian API guidelines.
- [Schema Editor](https://teamdigitale.github.io/dati-semantic-schema-editor/) supports editing JSON Schema,
  with visual navigation.

---

## Start with Metadata

In OAS we start by describing metadata, to clarify:

- API goals, audience and context;
- Terms of service;
- Versioning.

This step ensures that:

- goal and audience are clear,
  and you can actually write a meaningful description of your service,
  of its boundaries and context of use;
- legal and organizational requirements are taken into account from the beginning
  (eg. terms of service, GDPR, etc.);

The metadata is in the `info` section:

```yaml
openapi: 3.0.0
info:
  version: "1.0.0"
  title: |-
    Write a short, clear name of your service.
  description: |
    This field may contain the markdown documentation of the API,
    including references to other docs and examples.
  #
  # Legal references and terms of services.
  #
  termsOfService: 'http://swagger.io/terms/'
  contact:
    email: robipolli@gmail.com
    name: Roberto Polli
    url: https://github.com/ioggstream
  license:
    name: Apache 2.0
    url: 'http://www.apache.org/licenses/LICENSE-2.0.html'
```

----

## OpenAPI Metadata exercise

1. open [this incomplete OAS3 spec](https://editor.swagger.io/?url=https://raw.githubusercontent.com/ioggstream/python-course/main/connexion-101/notebooks/oas3/ex-01-info.yaml).

1. fix all errors and add the missing fields: no need to add all details for now.

1. describe the first API we're going to implement: a service which returns the current
   timestamp in [RFC5454](https://tools.ietf.org/html/rfc5424#section-6.2.3)
   UTC (eg. `2019-01-01T00:00:00Z`).

1. provide contact informations and terms of services.

1. Feel free to add as many details as you want.

----

### Custom fields

Specific ecosystems may add custom OAS fields via the `x-` prefix.
This should be done with care, to avoid clashes between different ecosystems.

When using custom fields, consider prefixing them
with a common namespace, eg. `x-acme-` to avoid clashes with other ecosystems.

:warning: OAS 3.1 introduced the concept of extension
fields: these should be "registered" and should not use
the `x-` prefix. We won't go into these details during
this course.

To backport new fields from OAS3.1 to OAS3.0, you can use custom fields, eg. `x-summary` for the `summary` field:

----

#### Lifecycle management

An API ecosystem needs a way to publish core lifecycle events, such as deprecation and retirement.
This allows users to have the time to adapt to changes

HTTP provides a couple of standard headers for `Deprecation` and `Sunset`
while most of the lifecycle management is left to the API providers.

**x-api-id** you may want to assign a time-persistend UUID to your API, so that you can change its `title` in the future.

```yaml
x-acme-api-id: 00000000-0000-0000-0000-000000000000
```

Other custom fields could provide ecosystem-specific information,
such as GDPR roles or geodata references.
achine readable format

---

## OpenAPI Metadata exercise: 2

1. open [the previous OAS3 spec](/edit/notebooks/oas3/ex-01-info.yaml).

1. copy its content in the [Swagger Editor Online]({oas_editor_url('')}).

1. provide further informations via custom fields: if you think of any interesting
   label, define them and comment properly using `#`

## Feature gap

OAS 3 does not support the following features:

- API lifecycle management (eg. sandboxing, deprecation, retirement, ..)
- TODO: Healthcheck metadata, but you can use custom fields for that, eg. `x-healthcheck`:
  it makes sense to provide specific healthcheck endpoints to avoid that users
  use custom queries that may end up in performance issues or false expectations.
