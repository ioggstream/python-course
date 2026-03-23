# Throttling headers

Service management is an essential component of a stable API Ecosystem.

Basic compontents for service management are communicating:

- when you are not operational, and explicit
  how long it will take to be up and running again;

- if they are over quota and
  prevent overquota via throttling headers.


While it could be annoying to explicitly state that every response
should contain throttling headers, you can use yaml anchors for that!

```
x-commons:
  throttling-headers: &throttling-headers
    X-RateLimit-Limit:
      $ref: ..
    X-RateLimit-Remaining:
      $ref: ..
    X-RateLimit-Reset:
      $ref: ..

```


## Returning throttling headers

Now we can use the anchor in our `get /echo responses`

```
paths:
  /echo
    get:
      ...
      operationId: api.get_echo
      responses:
        '200':
          headers:
            <<: *throttling_headers
          ...
```


### Exercise: add throttling headers

Modify the  [ex-07-01-throttling.yaml](/edit/notebooks/oas3/ex-07-01-throttling.yaml) spec so that:

- `get /echo responses` returns the throtting headers in case of `200`;
- ensure that in case of over-quota, a `429` response is returned

### Exercise: throttle requests in api.py

Use the `throttling_quota` utilities either:

- the throttle decorator
- or implement your own throttling


```
# Decorate with `throttle`
from oas3.throttling_quota import throttle

@throttle
def f(user='foo'):
    return {}, 200, {}

```


```
# Or write your own using
from oas3.throttling_quota import ThrottlingQuota

quotas = ThrottlingQuota(ttl=30, limit=3)

for i in range(4):
    ret = quotas.consume(user=f'user1')
    print(ret)
```

    {'limit': 3, 'remaining': 2, 'reset': 23, 'user': 'user1', 'comment': '2019-07-06T07:57:00'}
    {'limit': 3, 'remaining': 1, 'reset': 23, 'user': 'user1', 'comment': '2019-07-06T07:57:00'}
    {'limit': 3, 'remaining': 0, 'reset': 23, 'user': 'user1', 'comment': '2019-07-06T07:57:00'}
    {'limit': 3, 'remaining': 0, 'reset': 23, 'user': 'user1', 'comment': '2019-07-06T07:57:00'}


Modify [api.py:get_echo](/edit/notebooks/oas3/api.py) such that:

- every authenticated user get its quota;
- if quota is exceeded, `429` is returned;
- the throttling infos are returned as integers in every response:

  - X-RateLimit-Limit: maximum number of requests in the given interval
  - X-RateLimit-Reset: when the quota expires
  - X-RateLimit-Remaining: remaining requests before the quota is consumed


Now  [run the spec in a terminal](/terminals/1) using

```
cd /code/notebooks/oas3/
connexion run /code/notebooks/oas3/ex-07-01-throttling-ok.yaml
```

play a bit with the [Swagger UI](https://TODO)

and try making a request!



```
!curl http://localhost:5000/datetime/v1/echo -kv -ufoo:foo
```


```

```
