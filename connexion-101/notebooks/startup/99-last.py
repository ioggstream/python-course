# Load default libraries and functions in jupyter

from os import environ as env
from urllib.parse import urlparse

import yaml
from IPython.display import Markdown, display
from requests import get
r

def render_markdown(s):
    return display(Markdown(s))


#
# Useful constants
#
editor_url = f'http://{env["MAIN_IP"]}' + ":8080/?url="
api_url = f'http://{env["MAIN_IP"]}' + ":5000/"
defintions_yaml = (
    "https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml#/parameters"
)


def api_server_url(path):
    return api_url + path


def oas_editor_url(url):
    return editor_url + url
