# Response integrity with Content-Digest

```text
SPEC_FILE=ex-07-02-integrity-ok.yaml uvicorn api_solution:main  --reload
```

Service management is not only about availability and quotas.

Clients may also need a simple way to verify that the response body
they received is exactly the one produced by the server.

The HTTP fields `Want-Content-Digest` and `Content-Digest` can be used
for that purpose:

- the client sends `Want-Content-Digest` to ask for a digest in the response;

- the server replies with `Content-Digest`, containing the digest of the
  response body.

In this lesson we only focus on describing these headers in the API
contract. The implementation details of generating digests are out of scope.

While it could be annoying to explicitly state these headers every time,
you can define them once in shared components and reuse them from your
operations.

```yaml
components:
  parameters:
    Want-Content-Digest:
      $ref: 'components.oas3.yaml#/components/parameters/Want-Content-Digest'
  headers:
    Content-Digest:
      $ref: 'components.oas3.yaml#/components/headers/Content-Digest'
```

## Requesting response digests

Now we can use these reusable definitions in our `get /echo` operation.

```yaml
paths:
  /echo:
    get:
      parameters:
        - $ref: '#/components/parameters/tz'
        - $ref: '#/components/parameters/Want-Content-Digest'
      responses:
        '200':
          headers:
            Content-Digest:
              $ref: 'components.oas3.yaml#/components/headers/Content-Digest'
          ...
```

### Exercise: document integrity headers

Read the [ex-07-02-integrity-ok.yaml](/edit/notebooks/oas3/ex-07-02-integrity-ok.yaml)
spec and identify:

- where the `Want-Content-Digest` request header is declared;
- where the `Content-Digest` response header is returned;
- how the `get /echo` description explains this behavior to clients.

### Exercise: run the API contract

Run the spec in a terminal using:

```text
connexion run /code/notebooks/oas3/ex-07-02-integrity-ok.yaml
```

Then inspect the API from Swagger UI and try sending a request with
the `Want-Content-Digest` header.

For example:

```python
!curl http://localhost:5000/datetime/v1/echo -kv -ufoo:foo \
  -H 'Want-Content-Digest: sha-256=1'
```

Check whether the response documents and exposes a `Content-Digest`
header, and discuss how a client could use it to verify integrity.