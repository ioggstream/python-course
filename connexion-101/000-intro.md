# Interoperable REST APIs with OpenAPI 3 and Connexion

Welcome to the API-First training!

[Intro slides](https://docs.google.com/presentation/d/1c_pH0nVY5WwMOlMpr0vaeC1Mblpw-HvffvuECQgH4Yc/edit#slide=id.p4)

## Agenda

- [x] Course environment
- [x] [Interoperability](/notebooks/notebooks/010-interoperable-apis.ipynb): Goals, REST, RPC, Contract First.
- [x] [API modeling with OpenAPI 3](/notebooks/notebooks/025-openapi-3.ipynb)
- [x] [The `connexion` framework](/notebooks/notebooks/030-connexion.ipynb),
   mocking our API model, returning Problem objects
- [x] [Implementing the endpoints without request parameters](/notebooks/notebooks/040-01-connexion-writing-operationid.ipynb) and [with request parameters](/notebooks/notebooks/040-02-connexion-writing-operationid.ipynb)
- [x] [Using YAML features and `$ref` to enforce API behavior](/notebooks/notebooks/050-reusing-and-bundling.ipynb)
- [x] Authorization: [basic auth](/notebooks/notebooks/060-security-confidentiality.ipynb)
- [x] Service management with [ratelimit headers](/notebooks/notebooks/070-security-availability.ipynb)
- [x] [Pagination](/notebooks/notebooks/080-connexion-pagination.ipynb)
- [ ] [Validation intro](/notebooks/notebooks/090-connexion-validation.ipynb)

Bonus tracks:

- [x] Authorization with JWT

## Strategy

We will adopt an iterative strategy, progressively:

1. introduce more OAS3 features
2. write OAS3 specifications
3. implement the associated code
4. repeat

## Jupyter

is the course environment in your browser.

It's not a way for not doing your homework ;)

You can:

- [open a terminal on the local machine](/terminals/example)
- [edit an existing file](/edit/notebooks/untitled.txt)
- add more cells with `ALT+ENTER`

FIXME: Go to the [basic python course](/tree/notebooks/rendered_notebooks/python-basic)

## Course services and directories

- IP:`8888/notebooks`  this Jupyter notebook
- IP:`5000`  the flask application we will execute during the course

Once you open the [terminal](/terminals/connexion) you will find the course under:

- `notebooks` if you run it locally;
- `/code/notebooks` if you are on docker

```text
/code/
│  
└── notebooks    # All notebooks!
    ├── oas3     # OpenAPI specifications, files and exercises
    │  
    └── startup  # startup files for jupyter, don't touch ;)
```

---

## Customizing the app

To simplify things, during the training we'll run the connexion app with the `connexion run` command.


Whenever you complete an exercise, you should run
the API with:

```text
connexion run oas3/openapi.yaml
```

Not covered in this workshop:
if you need to tweak your application,
you can still create a connexion app
and run it with an `asgi` container:

```python
from connexion import AsyncApp

def main():
    """
    Run me with
    $ uvicorn api:main --port ...
    """
    app = AsyncApp(...)
    app.add_api( ...)
    ...
    return app
```



## If you can't do an exercise

During the course we'll write two files:

- openapi.yaml with the API specifications;
- api.py with the API implementation

You can find solutions in the training directory, so if you can't complete your openapi.yaml
you can run the solution (which ends with `-ok.yaml` instead, with

```text
connexion run oas3/ex-03-02-path-ok.yaml
```


---

## Clone and start

```text
git clone https://github.com/ioggstream/python-course.git
cd python-course/connexion-101
```

## Connect to jupyter

```text
open http://localhost:8888/tree/notebooks/?token=....
```
