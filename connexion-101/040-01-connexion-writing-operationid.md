# Implementing methods

Once we have a mock server, we could already provide an interface to
external services mocking our replies.

This enables:

- clients to test our API
- quick feedbacks on data types and possible responses.

With the contract,
both we and our users
can start with the implementation!

---

## OperationId

OperationId is the OAS3 field that maps the resource-target with the python function to call.

```yaml
paths:
  /status
    get:
      ...
      operationId: api.get_status
      ...
```

----

The method signature should reflect the function's one.

OAS allows to pass parameters to the resource target via:

- query parameters
- http headers
- request content (aka body)

---

### Implement get_status

At first we'll just implement the `get_status` in [api.py](/edit/notebooks/oas3/api.py) function that:

- takes no input parameters;
- returns a problem+json

----

```python
# connexion provides a predefined problem object
from connexion import problem


# Exercise: write a get_status() returning a successful response to problem.
help(problem)
```

----

```python
def get_status():
    return problem(
        status=200,
        title="OK",
        detail="The application is working properly"
    )

```

Now  [run the spec in a terminal](/terminals/connexion) using

```text
connexion run /code/notebooks/oas3/ex-03-02-path.yaml
```

play a bit with the [Swagger UI](http://localhost:5000/datetime/v1/ui)
and try making a request!

```python
from requests import get
res = get("http://localhost:5000/datetime/v1/status")
print(res.headers)
print(res.content)
```
