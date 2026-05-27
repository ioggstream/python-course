# Interoperable REST APIs with OpenAPI 3 and Connexion

Welcome to the API-First training!

[Intro slides](https://docs.google.com/presentation/d/1c_pH0nVY5WwMOlMpr0vaeC1Mblpw-HvffvuECQgH4Yc/edit#slide=id.p4)

## Agenda

- [x] Course environment
- [x] [Interoperability](/notebooks/notebooks/01-interoperable-apis.ipynb): Goals, REST, RPC, Contract First.
- [x] [API modeling with OpenAPI 3](/notebooks/notebooks/02-openapi-3.ipynb)
- [x] [The `connexion` framework](/notebooks/notebooks/03-connexion.ipynb),
   mocking our API model, returning Problem objects
- [x] [Implementing the endpoints without request parameters](/notebooks/notebooks/04-01-connexion-writing-operationid.ipynb) and [with request parameters](http://192.168.1.115:8888/notebooks/notebooks/04-02-connexion-writing-operationid.ipynb)
- [x] [Using YAML features and `$ref` to enforce API behavior](/notebooks/notebooks/05-reusing-and-bundling.ipynb)
- [x] Authorization: [basic auth](/notebooks/notebooks/06-connexion-authorization-basic.ipynb)
- [x] Service management with [interoperabile throttling headers](/notebooks/notebooks/07-connexion-throttling-headers.ipynb)
- [x] [Pagination]s(/notebooks/notebooks/08-pagination.ipynb)
- [ ] [Validation intro](/notebooks/notebooks/09-connexion-validation.ipynb)

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
- IP:`8080` the API Documentation Web UI (Swagger UI)
- IP:`5000`  the flask application we will execute during the course

Once you open the [terminal](/terminal/1) you will find
all the course under `/code`.

```
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

You can always provide a custom `__main__.py` like you normally do with your apps (eg: enable TLS, ...).

Whenever you complete an exercise, you should run

```
connexion run /code/notebooks/oas3/openapi.yaml
```

## If you can't do an exercise

During the course we'll write two files:

- openapi.yaml with the API specifications;
- api.py with the API implementation

You can find solutions in the training directory, so if you can't complete your openapi.yaml
you can run the solution (which ends with `-ok.yaml` instead, with

```text
connexion run /code/notebooks/oas3/ex-03-02-path-ok.yaml
```

```python
# You can evaluate maths and strings
s = 1
print("a string and the number " + str(s))

s = s + 1
print("now s is increased " + str(s))
```

```python
# Note: all notebooks preload the definitions in
!ls -l /root/.ipython/profile_default/startup
```

---

## Clone and start

```
git clone https://github.com/ioggstream/python-course.git
cd python-course/ansible-101
make course

```

## Connect to jupyter

```
firefox http://43.32.54.212:8888/tree/notebooks/?token=....
```
