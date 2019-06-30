# Load default libraries and functions in jupyter

import json
import os
import sys
from os import environ as env
from pathlib import Path
from urllib.parse import urlparse

import yaml
from IPython.display import Latex, Markdown, display
from requests import get
from openapi_resolver import OpenapiResolver

def render_markdown(s):
    return display(Markdown(s))


#
# Useful constants
#
editor_url = f'http://{env["MAIN_IP"]}' + ":8080/?url="
api_url = f'http://{env["MAIN_IP"]}' + ":5000/"
defintions_yaml = "https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml#/parameters"


def api_server_url(path):
    return api_url + path

def oas_editor_url(url):
    return editor_url + url



def show_component(url):
    U = urlparse(url)
    fragment = U.fragment.strip('/').split('/')
    ret = yaml.safe_load(get(url).content)
    for k in fragment:
        ret = ret[k]
    return OpenapiResolver.yaml_dump_pretty(ret)

