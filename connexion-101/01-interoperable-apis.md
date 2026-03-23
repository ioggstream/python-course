# Interoperable APIs

The Italian Government - like other Countries - is standardizing REST APIs to create an uniform developer experience for software provided by its:

- 20 Regions
- 8_000 municipalities
- 20_000 local and central agencies

At the core of this interoperability strategy we have:

- API First Approach based on OpenAPI v3
- HTTPS everywhere
- Service Management with standardized throttling and circuit-breaker patterns
- Standardized approach to metrics

[See Slides](https://docs.google.com/presentation/d/1L6R4ZKhLoZAPEmai1KSED1nrq0GNrx3-TU53sGhfrO8/edit#slide=id.g3aa6058ea8_0_0)

## Agenda

In this training we'll show how to:

- model interoperable APIs
- leverage interoperability by reuse

We'll use [connexion](https://github.com/spec-first/connexion), a python framework which streamlines API creation.

# REST and RPC

The historical API approach was to view any interaction like a function call.

In a network environment this is seen as a `Remote Procedure Call`,
used by:

- SOAP web services, that use XML as a data format and HTTP as a transport protocol;
- GRPC, that uses HTTP/2 as a transport protocol and Protocol Buffers as a data format.

The widespread of HTTP as a distributed computation protocol, and the rise of data give birth to REST.

REST, aka REpresentation State Transfer, is not a protocol, but an architectural style which mimics the distributed characteristics of the web.

In REST, everything is a [resource](https://ietf.org/rfc/rfc9110.html#name-resources):

- identified by an Uniform Resource Locator URL;
- which is conveyed by a `representation`. A given resource could be represented as `application/json` or as [`application/xml`](https://tools.ietf.org/html/rfc7303), in different languages (see `Content-Language`) and differently encoded (see `Content-Encoding`);
- whose state is transferred between an Origin Server and a User Agent (see RFC7230);

There are no "functions" but everything is modeled as a resource.
Moreover all the HTTP semantics ([RFC9110](https://datatracker.ietf.org/doc/html/rfc9110)) applies, including idempotent and non-idempotent methods and caching.

The REST architectural style **leverages the distributed nature of the web**
and the features of HTTP which are redesigned with REST in mind (see RFC911x).

While REST is not a silver bullet, we **acknowledged that public services are usually about data and resources** making a REST style a good approach in service modeling.

Moreover a semantic approach to URIs simplifies routing and auditing based on http status, method and path.

# Describing APIs

Providing **usable** digital services requires:

- publishing interfaces;
- involve stakeholders/users in the service lifecycle.

You must **COMMUNICATE**:

- technical specifications;
- service metadata;
- documents and references.

## Interface Description Language

Digital service description requires an Interface Description Language.
That's a **machine readable language** that describes the interface.

**For REST APIs, the standard IDL is OpenAPI, aka OAS**.

For example, a web service accepting the following request `GET /echo` and returning a json object could be described in OAS3 like the following:

```yaml
...
paths:
  /echo:
    get:
      responses:
        "200":
          application/json: {}
...
```

This disambiguates the API definitions and usage.

## Contract first, Code first

There are two paths towards API implementation:

- Code First: where one develops a function on a specific language and then uses some tool to generate the
  IDL. An example function generating the above IDL could be

  ```python
  def echo():
      item = {"hello": "world"}
      status_code = 200
      headers = {'content-type': 'application/json'}

      return item, status_code, headers
  ```

  This is the approach used by many frameworks,
  and that is NOT the one we use in this training.
  Moreover, this approach is strongly discouraged in a large ecosystem.

- Contract First: one writes down the interface in an IDL, then let the tools generate the code stubs
  or the wiring.

## Contract first improves standardization

While code-first has a lot of traction between developers, as they could focus on writing the actual code
and leave the interface (and documentation) as an underproduct, this approach rarely works in a large ecosystem where

- different actors
- in a long timeframe
- works with different frameworks and enviroments.

A contract-first approach, instead:

- allows to focus on the actual design of the API,
  without being entangled by implementation details;
- it's independent from the framework and language people use for their client/server implementation
  and from how frameworks generate the specs (which may be buggy);

Focusing on the specs allows to create *API modeling iterations*
that enable the API to change fast
and involve stakeholders in the modeling and in the API lifecycle.

NB: this doesn't mean iterations don't involve testing that the actual code works ;)

# Interoperability requirements

A sane API ecosystem requires basic standardization features, such as:

- API-first/Contract-first approach, with documentation and interface description as a first class citizen;

- Catalogs for API and Data schemas;

- Standardization of data formats, including dates and log timestamping format;

- Availability strategy based on a distributed circuit-breaker and throttling patterns;
