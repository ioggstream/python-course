# Authorization & securitySchemes

OAS allows to specify authorization policies in the spec,
under `components.securitySchemes`.

Between supported security schemes we have:

- oauth and oidc
- basic auth
- JWT
- mutualTLS ( in OAS 3.1 )

**When passing credentials in HTTP headers or payload you MUST use TLS**

`connexion` can reference a python function via `x-basicInfoFunc`.
Authenticated operations gets user informations via the `user` parameter.

### OAS3: basic auth

Here we are defining the `myBasicAuth` security scheme.

```yaml
components:
 securitySchemes:
   myBasicAuth:
     type: http
     scheme: basic
     x-basicInfoFunc: security.my_auth
```

We can then reference `myBasicAuth` in one or more paths

```yaml
paths:
  /echo
    get:
      security:
      - myBasicAuth: []
      ...
      operationId: api.get_echo
      ...
```

### OAS3 Exercise: add securitySchemes

Modify the OAS3 spec in [ex-06-01-auth.yaml](/edit/notebooks/oas3/ex-06-01-auth-ok.yaml) and:

- add a `myBasicAuth` security schemes like the above;
- reference `myBasicAuth` in `get /echo` path;
- validate the spec in your swagger editor and
  check what changed in the swagger-ui

### Implement my_auth

Implement the `my_auth` function in [security.py](/edit/notebooks/oas3/security.py) so that:

- when `username == password` the user is authenticated

Use the cell below to implement it,

```python
# Test here the my_auth implementation.
def my_auth(username, password,required_scopes=None):
    """An dummy authentication function.
       :params: username, the username
       :params: password, the password
       :params: scopes, the scope
       :returns: `{"sub": username, "scope": ""}` on success,
                 None on failure
    """
    raise NotImplementedError

```

### Add `user` support in get_echo

Operations like `get_echo` gets user informations via the `user` param.

Modify get_echo in [api.py](/edit/notebooks/oas3/api.py) such that:

- unauthenticated replies returns a `401` http status
- the authenticated reply contains user informations `{"timestamp": "2019-01-01T21:04:00Z", "user": "jon"}`

```python
def get_echo(tz, user=None):
    """
        :param: tz, the timezone
        :param: user, the authenticated user passed by `connexion`
    """
    raise NotImplementedError
```

### Test the my_auth implementation

Run the spec in the [terminal](/terminals/connexion)
with the usual

```
connexion run /code/notebooks/oas3/ex-06-01-auth-ok.yaml
```

```python
render_markdown(
f'''

Play a bit with
[Swagger UI]({api_server_url("ui")})

''')
```

```python
# Try to curl some requests!
!curl http://localhost:5000/datetime/v1/echo -kv
```

### Bearer token & JWT Security

Bearer tokens are supported:

- in OAS via the `scheme: bearer`
- in connexion via the `x-bearerInfoFunc`

```yaml
components:
  securitySchemes:
    jwt:
      type: http
      scheme: bearer
      bearerFormat: JWT
      x-bearerInfoFunc: security.decode_token

```

Once you send the header

`Authorization: Bearer token`

the `token` string will be passed to a function like the following

NOTE: the `bearerFormat` is a free identifier of the token format and the associated syntax may not be enforced by the spec.

```python
def decode_token(token):
    """
        :param: token, a generic token
        :return: a json object compliant with RFC7662 OAUTH2
    """

    if token_is_valid:
        return {
             'iss': 'http://api.example.com',
             'iat': 1561296569,
             'exp': 1561296571,
             'sub': 'ioggstream',
             'scope': ['local']
            }
```

You can learn more on Connexion Security on:

- <https://github.com/zalando/connexion/blob/master/docs/security.rst>

A complete JWT example is [here](https://github.com/zalando/connexion/blob/master/examples/openapi3/jwt/app.py)

```python

```
