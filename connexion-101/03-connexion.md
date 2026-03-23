# Connexion

[Connexion](https://github.com/spec-first/connexion) is a python framework which streamlines API creation
of contract-first REST APIs.

Once you have your OAS3 spec, `connexion` uses it to:

- dispatch requests
- serve mock responses on unimplemented methods
- validate input and output of the called methods
- apply authentication policies
- provide an API Documentation UI (Swagger UI) where we can browse our API.

```python
# At first ensure connexion is installed
# together with the swagger module used to render the OAS3 spec
# in the web-ui
!pip install connexion[swagger-ui] connexion
```

Now  [run the spec in a terminal](/terminals/1) using

```bash
connexion run /code/notebooks/oas3/ex-01-info-ok.yaml
```

Remember:

- default port is `:5000`
- the Swagger GUI is at the `/ui` path.


```python
# A request on a generic PATH on the server returns a
# nicely formatted and explicative error.
# Remember that we haven't already defined an operation.
!curl http://0.0.0.0:5000 -kv
```


```python
render_markdown(f'''
Open the [documentation URL]({api_server_url('ui')}) and check the outcome!

Play a bit with Swagger UI.''')

```

## Defining endpoints in OAS3

Now that we have added our metadata, we can **provide informations about the endpoints**.
OAS3 allows multiple endpoints because good APIs have many.

Every endpoint can start with a prefix path (eg. `/datetime/v1`).


```
# One or more server
#   You can add production, staging and test environments.
#   We
#   sandbox instances
servers:
  - description: |
      An interoperable API has many endpoints.
      One for development...
    url: https://localhost:8443/datetime/v1

  - description:
      One for testing in a sandboxed environment. This
      is especially important to avoid clients to
      test in production.
      We are using the custom `x-sandbox` to identify
    url: https://api.example.com/datetime/v1
    x-sandbox: true

  - description: |
      Then we have our production endpoint.
      The custom `x-healthCheck` parameter
      can be used to declare how to check the API.
    url: https://api.example.com/datetime/v1/status
    x-healthCheck:
      url: https://api.example.com/datetime/v1/status
      interval: 300
      timeout: 15

```

### Exercise: the `servers` parameter

Edit the `servers` attribute so that it points to your actual endpoint URL (eg. your IP/port).

Now check the outcome.

```
connexion run /code/notebooks/oas3/ex-02-servers-ok.yaml
```

## Defining `paths`

Now we can define our first `path` that is the `/status` one.

An interoperable API should declare an URL for checking its status.

This allows implementers to plan a suitable method for testing it (eg. it could be
a simple OK/KO method or can execute basic checks like. databases are reachable, smoke testing other components, ..)

## Caveats on `/status`

**NB: the `/status` path is not a replacement for proper monitoring your APIs, but a way to communicate to your peers that you're online.**

## Paths anatomy

An OAS3 path references:

- the associated METHOD (eg. get|post|..)
- a `summary` and a `description` of the operation


```
  /status:
    get:
      summary: Returns the application status.
      description: |
        This path can randomly return an error
        for testing purposes. The returned object
        is always a problem+json.
```

- a reference to the python object to call when the

```
      operationId: get_status
```

- the http statuses of the possible responses, each with its description,
  content-type and examples

```
      responses:
        '200':
          description: |
            The application is working properly.
          content:
            application/problem+json:
              example:
                status: 200
                title: OK
                detail: API is working properly.
        default:
          description: |
            If none of the above statuses is returned, then this applies
          content:
            application/problem+json:
              example:
                status: 500
                title: Internal Server Error
                detail: API is not responding correctly



```

### Exercise

- open the [ex-03-02-path.yaml](/edit/notebooks/oas3/ex-03-02-path.yaml)
  eventually copy/paste the code from/to the swagger editor.
- complete the `get /status` path

We haven't already implemented the function `get_status()` referenced by `operationId`,
so [to run the spec in a terminal](/terminals/1) we tell the server
to ignore this with `--stub`

```
connexion run /code/notebooks/oas3/ex-03-02-path.yaml --stub
```

### Exercise

1- What happens if I get the `/status` resource of my API now?

2- And if I invoke another path which is not mentioned in the spec?

3- Restart the server via

```
connexion run /code/notebooks/oas3/ex-03-02-path.yaml --mock notimplemented
```


```python
# Exercise:  what's the expected output of the following command?

!curl http://0.0.0.0:5000/datetime/v1/status

# Exercise: what happens if you GET an unexisting path?

!curl http://0.0.0.0:5000/datetime/v1/MISSING

```

Solution on the unimplemented method

```
$ curl http://0.0.0.0:8889/datetime/v1/status
{
  "detail": "Empty module name",
  "status": 501,
  "title": "Not Implemented",
  "type": "about:blank"
}
```

Solution on other paths

```
$ curl http://0.0.0.0:8889/datetime/v1/missing
{
  "detail": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
  "status": 404,
  "title": "Not Found",
  "type": "about:blank"
}
```

## Schemas

OAS3 allows defining, using and reusing schemas.

They can be defined inline,  in the `component` section or referenced from another file, like below.
The  URL fragment part can be used to navigate inside the yaml (eg. `#/schemas/Problem`).

```
components:
    schemas:
      Problem:
        $ref: 'https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml#/schemas/Problem'

```



```python
print(show_component('https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml#/schemas/Problem'))
```


```python
# Exercise: use the yaml and requests libraries
# to download the Problem schema
from requests import get
ret  = get('https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml')

# Yaml parse the definitions
definitions = yaml.safe_load(ret.content)

# Nicely print the Problem schema
print(yaml.dump(definitions['schemas']['Problem']))
```


```python
### Exercise
# Read the definitions above
# - https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml
#
# Then use this cell to list all the structures present in definitions
```


```python
for sections, v in definitions.items():
    for items, vv in v.items():
        print(f'{sections}.{items}')
```

## Exercise

Edit [ex-03-02-path.yaml](/edit/notebooks/oas3/ex-03-02-path.yaml) so that every `/status` response uses
the `Problem` schema.

Look at [simple.yaml](https://github.com/teamdigitale/api-starter-kit/blob/master/openapi/simple.yaml) to
see a complete implementation.


```python
## Exercise

#Test the new setup


```
