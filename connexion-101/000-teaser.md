# Mastering API Design at Scale

Welcome to Mastering API Design at Scale!
Author: <roberto.polli@par-tec.it>

---

## Hints

- **Type in** exercises so you can learn from your mistakes
- If your notebook get stuck, **restart the kernel and run all** cells
- **Repetita iuvant**: concepts will be explained multiple times,
  from different perspectives, thoughout various notebooks.

## Teaser

In this course, we will learn how to design resilient APIs
using OpenAPI and JSON Schema in a contract-first approach.

```python
%pip install connexion[swagger-ui] connexion[uvicorn] jsonschema openapi-spec-validator
```

(and some validation tools)

We will focus on API design, not on implementation,
since features can be implemented in different ways:

- programmatically,
- using frameworks,
- or architectural components such as API gateways.

We will always start from an API Specification.

```bash
cat oas3/simple.yaml
```

Use a contract-first API framework to test the design,
such as [Connexion](https://connexion.readthedocs.io/en/latest/)

To run an API server on

```python
from socket import gethostname, gethostbyname
hostname = gethostbyname(gethostname())
print(f"http://{hostname}:8080/ui")
```

open a [/terminal](/terminal) and run:

```text
connexion run --port 8080 --mock=all oas3/simple.yaml
```

... and contract-first tools to validate it, both statically
with Spectral

```bash
# Run via docker.
docker run --rm -v $(pwd):/app -w /app docker.io/stoplight/spectral lint openapi.yaml
```

and dynamically with Schemathesis (that can be even integrated in pytest.)

```python
!pip install schemathesis

!schemathesis run --checks all  http://{hostname}:8080/openapi.yaml```

We will also introduce JSON-LD and the concept of Semantic APIs
that allows referencing semantics to schemas,
to enable different API providers to align their APIs without
sharing the same schema.

```python
import yaml
spec = yaml.safe_load(open("oas3/person.yaml"))
schemas = spec["components"]["schemas"]
print(yaml.safe_dump(schemas))
```

You can create pydantic models from OAS3 schemas with [datamodel-code-generator](https://koxudaxi.github.io/datamodel-code-generator/)

```bash
pip install datamodel-code-generator
datamodel-codegen --input oas3/person.yaml --input-file-type openapi --output generated_model.py
cat generated_model.py
```

And some tools to visually navigate API Schemas:

- [Schema Editor](https://teamdigitale.github.io/dati-semantic-schema-editor/latest/#url=https://raw.githubusercontent.com/ioggstream/python-course/refs/heads/main/connexion-101/notebooks/oas3/person.yaml)
