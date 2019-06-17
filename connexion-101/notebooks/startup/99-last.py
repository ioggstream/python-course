# Load default libraries and functions in jupyter

from os import environ as env
import os
import sys
from IPython.display import display, Markdown, Latex
import yaml
import json
from pathlib import Path

def render_markdown(s):
    return display(Markdown(s))

#
# Useful constants
#
editor_url = f'http://{env["MAIN_IP"]}'+':8080/?url=' 

def oas_editor_url(url):
    return editor_url + url

