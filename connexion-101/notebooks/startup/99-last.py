# Load default libraries and functions in jupyter

from os import environ as env
import os
import sys
from IPython.display import display, Markdown, Latex

def render_markdown(s):
    return display(Markdown(s))
