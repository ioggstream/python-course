# Interoperable APIs

Writing APIs seems simple ... but what happens when
you have to maintain tens of APIs across different organizations, with different teams and frameworks?

This workshop is about creating an interoperable API ecosystem
with an uniform developer experience
for country-wide contexts.

---

In particular, this is based on the Italian public administration context, which includes:

- 20 Regions
- 8_000 municipalities
- 20_000 local and central agencies
- cross-border services with the European Union

---

## Interoperability requirements

An API ecosystem starts with communication requirements such as:

- Reliability & Security (e.g., CIA triad: Confidentiality, Integrity and Availability)
- Consistent Design & Schema Standardization

----

Basic standardization features to support these requirements include:

- API-first/Contract-first approach, with documentation and interface description as a first class citizen;

- Catalogs for API and Data schemas;

- Standardization of data formats, including dates and log timestamping format;

- Availability strategy based on a distributed circuit-breaker and throttling patterns;

<!-- Let's see how to manage such requirements -->
---

## REST and RPC

The historical API approach was to view any interaction like a function call.

In a network environment this is seen as a `Remote Procedure Call`,
used by:

- SOAP web services, that use XML as a data format and HTTP as a transport protocol;
- gRPC, that uses HTTP/2 as a transport protocol and Protocol Buffers as a data format.

----

The widespread of HTTP as a distributed computation protocol, and the rise of data give birth to REST.

REST, aka REpresentation State Transfer, is not a protocol,
but an architectural style which mimics the distributed characteristics of the web.

----

In REST, everything is a [resource](https://ietf.org/rfc/rfc9110.html#name-resources):

- identified by an **Uniform Resource Locator** (URL);
- conveyed by a **representation**.
  A resource can be represented in different formats, such as `application/json` or [`application/xml`](https://tools.ietf.org/html/rfc7303),
  in different languages (see `Content-Language`) and differently encoded (see `Content-Encoding`);
- whose state is transferred between an Origin Server and a User Agent (see RFC9110);

----

There are no "functions" but everything is modeled as a resource.
Moreover all the HTTP semantics ([RFC9110](https://datatracker.ietf.org/doc/html/rfc9110)) applies, including idempotent and non-idempotent methods and caching.

----

The REST architectural style **leverages the distributed nature of the web**
and the features of HTTP which are redesigned with REST in mind (see RFC911x).

**REST & Public services**: while REST is not a silver bullet, public services are usually about data:
this makes REST a good fit for modeling public services.

Moreover a semantic approach to URIs simplifies routing and auditing
based on http status, method and path.

---

## REST API & HTTP Standards

While we assume
that you are familiar with the HTTP protocol,
but just for a quick recap, here are some examples of HTTP requests and responses.

HTTP messages are composed by:

- a start line (request line or status line)
- headers (includes metadata about the representation, such as content type, content language, content encoding, etc.)
- an optional content

----


### HTTP Message Examples

A request to <http://api.example.com/datetime/v1/now>
for a resource representation in JSON format:

```http
GET /datetime/v1/now HTTP/1.1
Host: api.example.com
Accept: application/json
```

----

Response with a JSON representation of the current date and time:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 30

{
  "datetime": "2024-06-01T12:00:00Z"
}
```

----

The same resource could have more representations,
in different formats ...

```http
GET /datetime/v1/now HTTP/1.1
Host: api.example.com
Accept: text/plain
```

```http
HTTP/1.1 200 OK
Content-Type: text/plain

2024-06-01T12:00:00Z
```

----

Security features are usually implemented using HTTP functionalities
such as headers and status codes.

An authenticated request ...

```http
GET /datetime/v1/now HTTP/1.1
Host: api.example.com
Authorization: Bearer my-secret-token
```

Where the status code `401` indicates the error class.

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer
```

----

TODO: http ongoing work on API description:

- Integrity: Digest, HTTP Signatures, Unencoded Digest, etc.
- Discovery: Link header
- Error handling: Problem Details for HTTP APIs
- Security: QUERY method
- Efficiency: Resumable uploads

<https://datatracker.ietf.org/wg/httpapi/about/>

- lifecycle: Deprecation, Sunset, etc.
- catalog: RFC 9727
- YAML media type

---

## References

[See Slides]

- [Do we still need SOAP?](https://docs.google.com/presentation/d/1AqVoCmqVF4TrIw_QowEzdWh8F42wNZuHnIFyP3H2Qc0) [video](https://www.youtube.com/watch?v=9a2n8s1j5l0)
- [Extending HTTP for fun and non-profit](https://ep2020.europython.eu/talks/9mbcXTU-extending-http-for-fun-and-non-profit/)
- [Designing Secure APIs](https://ep2021.europython.eu/media/conference/slides/P8PaA9g-designing-secure-apis.pdf)
- [Self-explaining APIs](https://ep2021.europython.eu/media/conference/slides/9a2n8s1j5l0-self-explaining-apis.pdf)
