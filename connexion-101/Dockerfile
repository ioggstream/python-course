#
# Docker image for ipython notebook and various
#  python courses
#
FROM python:3.14-slim
LABEL maintainer="roberto.polli@par-tec.it"
RUN apt-get update && apt-get install -y git procps curl && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt /requirements.txt

# install requirements
RUN uv pip install --system -r /requirements.txt

# Use folding extension
RUN uv pip install --system jupyter_contrib_nbextensions

# Add API dependencies

COPY requirements-api.txt /requirements-api.txt
RUN uv pip install --system -r /requirements-api.txt

ENTRYPOINT ["/usr/local/bin/jupyter-notebook", "--ip", "0.0.0.0"]
