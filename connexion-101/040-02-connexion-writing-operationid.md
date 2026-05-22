# Implementing requests

Now we'll add new paths and add
request parameters, including
their schema.

Some parameters implement
common patterns, such as pagination parameters (`limit`, `offset`, `cursor`).
It is important to use the same set of
parameters across APIs to ease integration.

## A new path: /echo

Now we're going to write a new path: `/echo`.

- when invoking `/datetime/v1/echo` the API will return
  the current datetime;
- the response is enveloped in a json object:

```json
{ "timestamp": "2019-12-25T00:00:00Z" }
```

- the status code for a successful response is `200`

----

### Exercise: write /echo specs

Edit [ex-04-02-echo-ok.yaml](/edit/notebooks/oas3/ex-04-02-echo.yaml) and write the `echo` specifications:

1- define the new `Datetime` schema to be used in the response;

2- define the new `/echo` path supporting the `get` method and:

- always write proper `summary` and `description` fields

3- `get /echo` possible responses are:

- `200` returning a `Datetime` in json format, with a complete `example` for mocks
- `503` returning a `problem+json`

4- don't forget `operationId` !

Hint: feel free to reuse as much yaml code as possible.

----

### Exercise: test /echo mocks

Run your spec [in the terminal](/terminal/connexion) and check that it properly returns the mock objects.

Use

```text
connexion run --mock all /code/notebooks/oas3/ex-04-02-echo-ok.yaml
```

```python
# Use this cell to test the output
!curl http://localhost:5000/datetime/v1/echo -vk
```

---

## Request parameters

OAS3 allows to specify parameters both in `path`, `query` and  `headers`.

Interoperable APIs should follow simple rules when using parameters:

- define parameter conventions for common patterns, eg: `limit`, `offset`, `cursor`;
- use standard HTTP headers when possible.

----

We introduce the following pagination
parameters:

- `limit`: max number of entries to retrieve
- `offset`: the number of entries to skip in a paginated request
- `cursor`: an identifier (cursor) of the first entry to be returned
  [Slack APIs provide an example of cursor-based pagination](https://api.slack.com/docs/pagination)

---

## Adding request parameters to `/echo`

`Query` and `header` request parameters can be defined in

```yaml
components:
  parameters:
    a_sample_parameter:
      ...
```

```python
# Here's the `limit` parameter definition, including
# - it's a `query` parameter
# - its name
# - its schema
oas3 = yaml.safe_load(open("oas3/components.oas3.yaml"))
print(yaml.safe_dump(oas3["components"]["parameters"]["limit"]))
```

----

### Exercise: adding parameters to `/echo`

Let's add a `tz` parameter to `/echo`:

- create a `#/components/schemas/Timezone` schema definition. Valid example values are:

  - 'Europe/Rome'
  - 'UTC' (default)
  - 'Asia/Calcutta'

- create a `#/components/parameters/tz` parameter definition;
- add the `tz` query parameter to `get /echo` path checking
  the [official OAS 3.0.2 documentation](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#examples)
- add a `400 Bad Request` response in case the timezone is not in the list

Finally, check that you can run the spec.

```bash
connexion run --mock all /code/notebooks/oas3/ex-04-02-echo-ok.yaml
```

```python
# Use this cell to test your api
```

### Implement get_echo

Let's implement the `get_echo` in [api.py](/edit/notebooks/oas3/api.py) function that:

- takes the `tz` parameter, which defaults to `UTC`;
- returns a `Datetime` object in its current timezone.

```python
# hint: get the timezone from
!pip install pytz
```


```python
import pytz
tz = pytz.timezone('Europe/Rome')
print(tz.zone)
```

    Europe/Rome

```python
# No timezones in Neverland :)
'Neverland' in pytz.all_timezones
```

```python
### Exercise solution
```

```python
def get_echo(tz='UTC'):
    if tz not in pytz.all_timezones:
        return problem(
            status=400,
            title="Bad Timezone",
            detail="The specified timezone is not valid",
            ext={"valid_timezones": pytz.all_timezones}
        )
    d = datetime.now(tz=pytz.timezone(tz))
    return {"timestamp": d.isoformat().replace('+00:00', 'Z')}

```

Now  [run the spec in a terminal](/terminals/connexion) using

```
cd /code/notebooks/oas3/
connexion run /code/notebooks/oas3/ex-04-02-echo-ok.yaml
```

```python
render_markdown(f'''
play a bit with the [Swagger UI]({api_server_url('ui')})

and try making a request!
''')
```

```python
## TODO do we have enough time to show flask_testing?

# Check that default works
!curl http://localhost:5000/datetime/v1/echo -kv
```

```python
# Test a valid timezone
!curl http://localhost:5000/datetime/v1/echo?tz=Europe/Rome -kv
```


```python
# Test an invalid timezone
!curl http://localhost:5000/datetime/v1/echo?tz=Frittole -kv
```


```python

```
