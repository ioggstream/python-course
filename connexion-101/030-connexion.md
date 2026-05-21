# Connexion

[Connexion](https://github.com/spec-first/connexion) is a python framework
which streamlines API creation
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

## Running an API

Now  [run the spec in a terminal](/terminals/connexion) using

```python
import socket
host = socket.gethostbyname(socket.gethostname())
port = 5000
print(f"$ connexion run notebooks/oas3/ex-01-info-ok.yaml --host {host} --port {port}")
print()
print(f"Then open the documentation URL: http://{host}:{port}/ui")
```

Remember:

- default port is `:5000`
- the Swagger UI is at the `/ui` path.

----

```python
# A request on a generic PATH on the server returns a
# nicely formatted and explicative error.
# Remember that we haven't already defined an operation.
!curl http://0.0.0.0:5000 -kv
```

Open the [documentation URL]({api_server_url('ui')}) and check the outcome!

### Exercises {#connexion-run-ex}

- issue a `POST /ui` request and check that the status code is `405 Method Not Allowed`.
- issue a `GET /MISSING` request and check that the status code is `404 Not Found`.
- the `Content-Type` header field conveys the media type of the returned content;
  what's the content type of the error responses?

----

## Defining endpoints in OAS3

Now that we have added our metadata, we can **provide informations about server endpoints**.
OAS3 allows multiple server endpoints because
stakeholders interactions go through various lifecycle stages.

Every endpoint can start with a base path (eg. `/datetime/v1`).

```yaml
# One or more server
#   You can add production, staging and test environments.
#   A tip is to mark non-production instances as sandboxes.
servers:
  - description: |
      An interoperable API has many endpoints.
      One for development...
    url: https://localhost:8443/datetime/v1
    x-sandbox: true

  - description: |
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

----

### Exercise: the `servers` parameter

Edit the `servers` attribute so that it points to your actual endpoint URL (eg. your IP/port).

Now check the outcome in the [terminal](/terminals/connexion).

```text
connexion run /code/notebooks/oas3/ex-02-servers-ok.yaml
```

## Defining `paths`

Now we can define our first path that is the `/status` one.

An interoperable API should declare an URL for checking its status.

This allows implementers to plan a suitable method for testing it (eg. it could be
a simple OK/KO method or can execute basic checks like. databases are reachable, smoke testing other components, ..)

## Caveats on `/status`

**NB: the `/status` path is not a replacement for proper monitoring your APIs, but a way to communicate to your peers that you're online.**

## Paths anatomy

An OAS3 path references:

- the associated METHOD (eg. get|post|..)
- a `summary` and a `description` of the operation

```yaml
  /status:
    get:
      summary: Returns the application status.
      description: |
        This path can randomly return an error
        for testing purposes. The returned object
        is always a problem+json.
```

- a reference to the python object to call when the

```yaml
      operationId: get_status
```

- the http statuses of the possible responses, each with its description,
  content-type and examples

```yaml
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

### Exercise {#ex-status-stub}

- open the [ex-03-02-path.yaml](/edit/notebooks/oas3/ex-03-02-path.yaml)
  eventually copy/paste the code from/to the swagger editor.
- complete the `get /status` path

We haven't already implemented the function `get_status()` referenced by `operationId`,
so [to run the spec in a terminal](/terminals/1) we tell the server
to ignore this with `--stub`

```bash
connexion run /code/notebooks/oas3/ex-03-02-path.yaml --stub
```

### Exercise {#ex-status-mock}

1- What happens if I get the `/status` resource of my API now?

2- And if I invoke another path which is not mentioned in the spec?

3- Restart the server via

```bash
connexion run /code/notebooks/oas3/ex-03-02-path.yaml --mock notimplemented
```

```python
# Exercise:  what's the expected output of the following command?

!curl http://0.0.0.0:5000/datetime/v1/status

# Exercise: what happens if you GET an unexisting path?

!curl http://0.0.0.0:5000/datetime/v1/MISSING

```

Solution on the unimplemented method

```bash
$ curl http://0.0.0.0:8889/datetime/v1/status
{
  "detail": "Empty module name",
  "status": 501,
  "title": "Not Implemented",
  "type": "about:blank"
}
```

Solution on other paths

```bash
$ curl http://0.0.0.0:8889/datetime/v1/missing
{
  "detail": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
  "status": 404,
  "title": "Not Found",
  "type": "about:blank"
}
```
