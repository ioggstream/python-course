# Describing APIs

Interactions require communication,
and communication requires a common language,
and instructions on how the APIs can be used.

Providing **usable** digital services requires:

- publishing interfaces;
- involve stakeholders/users in the service lifecycle.

You must **COMMUNICATE**:

- technical specifications;
- service metadata;
- documents and references.

---

## Interface Description Language

Digital service description requires an Interface Description Language.
That's a **machine readable language** that describes the interface.

**For REST APIs, the standard IDL is OpenAPI Specification, aka OAS**.

----

Disambiguate API definitions and usage.

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

---

## Contract first, Code first

There are two paths towards API implementation

- Code First: we are not covering it today :)
- Contract First

----

### Code First

1. Develop language-specific code.
1. Code-specific tools generate the IDL.
1. Share the IDL to get feedback from stakeholders.

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

1. Very popular.
1. Discouraged in a large ecosystem :)

----

Lot of traction between developers,
as they could focus on writing the actual code
and leave the (boring) interface (and documentation) as an underproduct.

Rarely works in a large ecosystem where

- different actors
- in a long timeframe
- works with different frameworks and enviroments.

----

### Contract First

1. Write the interface in an IDL
  (a.k.a "The Contract")
1. Share and get feedback from stakeholders
1. Tools generate the code stubs or the wiring.
1. Implement the code.

----

Independent from the implementation language and framework.

Early feedback on the design and goals.

Still free to early implement the code to validate the design.

Stakeholders can implement clients
in parallel.

---

## Contract first improves standardization

A contract-first approach:

- focus on the actual design of the API
- lower entanglement with implementation details
- independent from the framework and language
  people use for their client/server implementation
  and from how frameworks generate the specs (which may be buggy);

----

Focusing on the specs allows to create *API modeling iterations*
that enable the API to change fast
and involve stakeholders in the modeling and in the API lifecycle.

----

Iterations *still* involve testing that the actual code works ;)
you can still write tests and stub implementation alongside the API modeling iterations
to ensure that both the API design supports both functional and non-functional requirements
such as reliability, security and performance.
