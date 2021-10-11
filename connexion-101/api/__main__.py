from logging import basicConfig
from os.path import dirname, isfile

from connexion import FlaskApp, problem
from yaml import safe_load as yaml_load


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


def configure_logger(log_config="logging.yaml"):
    """Configure the logging subsystem."""
    if not isfile(log_config):
        return basicConfig()

    from logging.config import dictConfig

    with open(log_config) as fh:
        log_config = yaml_load(fh)
        return dictConfig(log_config)


if __name__ == "__main__":
    configure_logger()
    app = FlaskApp(
        "hello",
        port=8443,
        specification_dir=dirname(__file__),
        options={"swagger_ui": True},
    )
    app.add_api("simple.yaml", validate_responses=True, strict_validation=True)
    app.run(ssl_context="adhoc", debug=True)
