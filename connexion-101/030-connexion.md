# Connexion

[Connexion](https://github.com/spec-first/connexion) is a python framework
which streamlines API creation
of contract-first REST APIs.

```python
# Install it with the swagger module
#   that renders the spec in a web-ui
!pip install connexion[swagger-ui] connexion

# And load some gobal settings for the exercises.
import socket
host = socket.gethostbyname(socket.gethostname())
port = 5000
```

----

`connexion` uses your OAS3 specification to:

- dispatch requests
- serve mock responses on unimplemented methods
- validate input and output of the called methods
- apply authentication policies
- provide an API Documentation UI (Swagger UI) where we can browse our API.

---

## Running an API

Now  [run the spec in a terminal](/terminals/connexion) using

```python
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

---

## Defining endpoints in OAS3

Now that we have added our metadata, we can **provide informations about server endpoints**.
OAS3 allows multiple server endpoints because
stakeholders interactions go through various lifecycle stages.

Every endpoint can start with a base path (eg. `/datetime/v1`).

---
-
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

[Edit the `servers` attribute](/edit/notebooks/oas3/ex-02-servers.yaml) and make it point to:

- the `/datetime/v1` base path;
- your actual endpoint URL (eg. your IP/port).

Now check the outcome in the [terminal](/terminals/connexion).

```python
# Use ex-02-servers-ok.yaml as a reference if you get stuck.
print(f"$ connexion run notebooks/oas3/ex-02-servers.yaml --host {host} --port {port}")
```

---

## Defining `paths`

The `paths` section declares the API endpoints and their operations.
Our first path that is the `/status` one,
that is used for health-checking the API.

This allows implementers to plan a suitable method for testing it (eg. it could be
a simple OK/KO method or can execute basic checks like: databases are reachable, smoke testing other components, ..)

----

### Caveats on `/status`

**NB: the `/status` path is not a replacement for proper monitoring your APIs, but a way to communicate to your peers that you're online.**

Without it, clients may implement custom ways to check your API,
such as issuing real requests (e.g. `GET /datetime/v1/now`)
that may result in unintended side effects (e.g., hitting always the same
database entries, hitting caches, ..).

----

## Paths anatomy

`paths` references:

- the associated METHODs (eg. get|post|..)
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

----

- an identifier, that `connexion` uses to map to the python callable

```yaml
      operationId: get_status
```

----

- the HTTP statuses of the possible responses, each with its description,
  media type and **examples**

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

----

### Exercise {#ex-status-stub}

- open [ex-03-02-path.yaml](/edit/notebooks/oas3/ex-03-02-path.yaml)
  eventually copy/paste the code from/to the swagger editor.
- complete the `get /status` path
- use the [OAS Checker](https://italia.github.io/api-oas-checker/)
  :warning: with the "Italian Guidelines Full + Extra Security Checks" profile
  to identify and fix syntax errors.
- what's the name of the function referenced by `#/paths/status/get/operationId`?

We haven't implemented the function referenced by `operationId`,
so [to run the spec in a terminal](/terminals/connexion)
we tell `connexion` to ignore unimplemented methods with `--mock notimplemented`:

```python
(
"bash$"
"connexion run notebooks/oas3/ex-03-02-path.yaml"
f" --host {host} --port {port}"
" --mock notimplemented"
)
```

----

### Exercise {#ex-status-mock}

1. What happens if I get the `/status` resource of my API now?
1. And if I invoke another path which is not mentioned in the spec?
1. Edit [api.py](/edit/notebooks/oas3/api.py) and rename `_get_status` function
   to `get_status`.
   What happens if you call the `/status` resource now?
1. Restart the server using `--mock all` and call `/status` again.
   What happens now?

```python
# Exercise: what's the expected output of the following command?
!curl http://0.0.0.0:5000/datetime/v1/status
```

```python
# Exercise: what happens if you GET an unexisting path?
!curl http://0.0.0.0:5000/datetime/v1/MISSING
```

----

### Exercise {#ex-status-impl}

1. Implement the `get_status` function in [api.py](/edit/notebooks/oas3/api.py)
   to return a problem+json with status 200, title "OK" and a successful
   message in detail.
1. Modify `get_status` to return `503` (Service Temporarily Unavailable) 1 in 5 requests.
