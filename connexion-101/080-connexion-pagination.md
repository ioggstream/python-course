# Pagination and encapsulation:

In our standardization policy, we defined a common set of pagination parameters.

Moreover we stated that responses should always be enclosed in json objects, eg:

* always return something that is extensible like

```http
GET /timezones

{
 "entries": [ "you", "can", "always", "add", "new", "keys" ]
}

```

* don't return `string`, `number` or `array`, because

```http
GET /dont-do-this

[ "you can't", "extend them"]
```

---

## Support pagination in `get /timezones`

We want to provide a `/timezones` path listing all the timezones supported
by `get /echo`

Our goal is the following:

- when invoking `/datetime/v1/timezones` the API will return
  the supported timezones in `pytz.all_timezones`;
- to limit resource consumption the server will return:
   * by default 5 entries
   * at most 10 entries
- the response is enveloped in the following example json object:

```
{
  "entries": [ "Europe/Rome", "UTC", .. ],
  "count": 5,
  "offset": 10
}
```

- the status code for a successful response is `200`

----

:warning: pagination should be implemented using a common
set of parameters to use. Our choice is:

- limit: max number of entries to retrieve
- offset: the number of entries to skip in a paginated request
- cursor: an identifier (cursor) of the first entry to be returned
  [Slack APIs provide an example of cursor-based pagination](https://api.slack.com/docs/pagination)

----

### Exercise: write /timezone specs

Edit the [ex-08-pagination-ok.yaml](/edit/notebooks/oas3/ex-08-pagination-ok.yaml) and write the `timezones` specifications:

1. define the new `Timezones` schema to be used in the response;

2. define the new `/timezones` path supporting the `get` method:

  * always write proper `summary` and `description` fields

3. `get /timezones` possible responses are:

  * `200` returning a `Timezones` in json format, with a complete `example` for mocks
  * `429` and `503` returning a `problem+json`

4. this operation is not authenticated

5. don't forget `operationId: get_timezones` !

Hint: feel free to reuse as much yaml code as possible.

----

### Exercise: test /timezones mocks

Run your spec [in the terminal](/terminals/connexion) and check that it properly returns the mock objects.

Use

```test
connexion run --mock all /code/notebooks/oas3/ex-08-pagination-ok.yaml
```


```python
# Use this cell to test the output
!curl http://localhost:5000/datetime/v1/timezones -vk
```

    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/timezones HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Content-Type: application/json
    < Content-Length: 117
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Fri, 05 Jul 2019 12:47:47 GMT
    <
    {
      "count": 3,
      "entries": [
        "Europe/Rome",
        "Asia/Calcutta",
        "UTC"
      ],
      "limit": 3,
      "offset": 10
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0

---

## Path parameters

OAS3 allows to specify `path` parameters:

 - in the path, with braces eg. `{continent}`
 - in `parameters` with the remaining details.


 **REMEMBER: path parameters are always required so you must define a new path
   and a new operationId: get_timezones_by_continent**


```
paths:
  /timezones/{continent}:
    get:
      ...
      parameters:
      - name: continent
        in: path
        required: true
        schema:
          type: string
  /timezones:
    ...
    definition without path-parameters
    ...
```

----

### Exercise: adding `path` parameter to `/timezones`

Let's add a `continent` path parameter to `/timezones`:

- create a `#/components/parameters/continent_path` parameter definition;
- add the `continent_path` query parameter to `get /timezones/{continent}` path checking
  the [official OAS 3.0.2 documentation](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#examples)
- add a `404 Not Found` response in case the continent is not present

Finally, check that you can run the spec.

```
connexion run --mock all /code/notebooks/oas3/ex-08-pagination-ok.yaml
```


```python
# Use this cell to test your api
```
----

### Exercise:  implement get_timezones operations

Let's implement the `get_timezones` operation in [api.py](/edit/notebooks/oas3/api.py) such that:

- is throttled
- takes the `limit` and `offset` parameters;
- returns a `Timezones` object containing all the timezones in pytz.all_timezones between offset and offset+limit


```python
# Check that default works
!curl http://localhost:5000/datetime/v1/timezones -kv
```

----

### Exercise:  implement get_timezones_by_continent operations

Let's implement the `get_timezones_by_continent` operation in [api.py](/edit/notebooks/oas3/api.py) such that:

- extends `get_timezones` behavior;
- returns a `Timezones` object containing all the timezones in the given continent, eg:

  * `Europe` -> ` [ "Europe/London", "Europe/Rome", ... ]`


```python
### Exercise solution

```


```python
!grep  '^def get_timezones' oas3/api-solution.py -A20 -B1
```

    @throttle
    def get_timezones(limit=5, offset=0, continent=None):
        entries = ALL_TIMEZONES

        if continent is not None:
            continent = str(continent).capitalize() + "/"
            entries = [x for x in entries if x.startswith(continent)]

        entries = entries[offset : offset + limit]
        return {
            "limit": limit,
            "offset": offset,
            "entries": entries,
            "count": len(entries),
        }


    @throttle
    def get_timezone(limit=5, offset=0, continent=None):
        return get_timezones(limit, offset, continent)


Now  [run the spec in a terminal](/terminals/connexion) using

```text
cd /code/notebooks/oas3/
connexion run /code/notebooks/oas3/ex-08-pagination-ok.yaml
```

TODO
```python
render_markdown(f'''
Play a bit with the [Swagger UI]({api_server_url('ui')})

and try making a request!
''')
```



Play a bit with the [Swagger UI](http://192.168.0.15:5000/ui)

and try making a request!




```python
# Use out-of-bound offset
!curl http://localhost:5000/datetime/v1/timezones?offset=800 -kv

# Pick in the middle
!curl 'http://localhost:5000/datetime/v1/timezones?offset=450&limit=2' -kv

# Pick in the middle
!curl 'http://localhost:5000/datetime/v1/timezones/Europe?limit=2' -kv

```

    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/timezones?offset=800 HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < X-RateLimit-Limit: 10
    < X-RateLimit-Remaining: 10
    < X-RateLimit-Reset: 1
    < Content-Type: application/json
    < Content-Length: 65
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Sat, 06 Jul 2019 15:01:18 GMT
    <
    {
      "count": 0,
      "entries": [],
      "limit": 5,
      "offset": 800
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0
    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/timezones?offset=450&limit=2 HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < X-RateLimit-Limit: 10
    < X-RateLimit-Remaining: 9
    < X-RateLimit-Reset: 0
    < Content-Type: application/json
    < Content-Length: 113
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Sat, 06 Jul 2019 15:01:19 GMT
    <
    {
      "count": 2,
      "entries": [
        "Europe/London",
        "Europe/Luxembourg"
      ],
      "limit": 2,
      "offset": 450
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0
    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/timezones/Europe?limit=2 HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < X-RateLimit-Limit: 10
    < X-RateLimit-Remaining: 8
    < X-RateLimit-Reset: 0
    < Content-Type: application/json
    < Content-Length: 111
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Sat, 06 Jul 2019 15:01:19 GMT
    <
    {
      "count": 2,
      "entries": [
        "Europe/Amsterdam",
        "Europe/Andorra"
      ],
      "limit": 2,
      "offset": 0
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0



```python

```
