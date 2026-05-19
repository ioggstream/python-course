# Describing APIs

<!--
So, we are going to build a lot of APIs that should interact
with each other to create a digital ecosystem.

Interactions require communication, and communication requires a common language,
and instructions on how the APIs can be used.
-->

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

**For REST APIs, the standard IDL is OpenAPI Specification, aka OAS**.

For example, a web service accepting the following request `GET /echo` and returning a json object could be described in OAS3 like the following:

```yaml
openapi: 3.0.0
...
paths:
  /echo:
    get:
      description: Reply with the request content.
      responses:
        "200":
          application/json: {}
...
```

This disambiguates the API definitions and usage.

## Contract first, Code first

There are two paths towards API implementation:

- Code First: you develop a function in a specific language
  and then use some tool to generate the IDL.
  An example function generating the above IDL could be

  ```python
  @app.post("/echo")
  def echo(body):
      """
      Reply with the request content.
      """
      item = {"hello": body}
      status_code = 200
      headers = {'content-type': 'application/json'}

      return item, status_code, headers
  ```

  This approach is very popular, but it strongly
  discouraged in a large ecosystem :)
  We are NOT covering this today.

- Contract First: you write down the interface in an IDL
  (a.k.a "The Contract"), share it with the stakeholders,
  and then let the tools generate the code stubs or the wiring.

## Contract first improves standardization

Code-first has a lot of traction between developers,
as they could focus on writing the actual code
and leave the interface (and documentation) as an underproduct.
This approach rarely works in a large ecosystem where

- different actors
- in a long timeframe
- works with different frameworks and enviroments.

A contract-first approach, instead:

- allows to focus on the actual design of the API,
  without being entangled by implementation details;
- it's independent from the framework and language
  people use for their client/server implementation
  and from how frameworks generate the specs (which may be buggy);

Focusing on the specs allows to create *API modeling iterations*
that enable the API to change fast
and involve stakeholders in the modeling and in the API lifecycle.

NB: this doesn't mean iterations don't involve testing that the actual code works ;)
you can still write tests and stub implementation alongside the API modeling iterations
to ensure that both the API design supports both functional and non-functional requirements
such as reliability, security and performance.
