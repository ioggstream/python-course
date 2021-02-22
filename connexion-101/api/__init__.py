from connexion import FlaskApp, problem
from os.path import isfile, dirname
from yaml import safe_load as yaml_load
from logging import basicConfig


def basic_auth(username, password, required_scopes=None):
    if username == password:
        return {"sub": username, "scope": ""}
    return None


def forward_token():
    raise NotImplementedError


def get_hello():
    """Connexion processes the yaml, and
         executes `get_hello`
    """
    return {"hello": "world"}


def get_hello_auth():
    """Connexion processes the yaml, and
         executes `get_hello`
    """
    return {"hello": "world"}


def post_hello(body):
    if not body:
        return problem(
            status=400, title="Bad Request", detail="Body should be a json object."
        )
    print(f"body, {body.__class__}")
    return {"UNEXPECTED_STRING": 1}

