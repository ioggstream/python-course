# Validation

Connexion supports validating request parameters and returned items
with:

```text
connexion run --strict-validation  oas3/ex-08-pagination-ok.yaml

```

----

### Exercise: test the current spec with invalid requests.

- invoke endpoints with unexisting parameters, eg. `/echo?missing=1`
- pass string values to numeric parameters


---

## Response validation

Connexion can shield us from non-conformant API implementation and
allow us to **validate responses** too. If the response is
not conformant to the OAS spec, connexion returns an error.


```text
connexion run --strict-validation --validate-responses /code/notebooks/oas3/ex-08-pagination-ok.yaml
```

----

### Exercise: test response validation

What happens when you?

- disable throtting on one of your operations, so that it won't return the 'X-RateLimit' headers;
- add new properties to the returned object?
- change the properties' returned type?

Does `connexion` always behave as you expected?

----

### Caveats

Validation can be tricky as you may have different requirements and connexion behavior may not fit your goals.

Connexion validators are quite tolerant, but you can write your own extending a validator class (eg. for request body, parameters, responses, ...)

```python
from connexion.decorators.validation import (
    RequestBodyValidator,
    ResponseBodyValidator,
    ParameterValidator)

def CustomBodyValidator(RequestBodyValidator):
    raise NotImplementedError

def main():
    app = AsyncApp(...)
    app.add_api("simple.yaml",
          validate_responses=True,
          validator_map={
               'body': CustomBodyValidator,
           }
     )
```
