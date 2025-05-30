FROM docker.io/library/python:3.12
COPY requirements.txt /
RUN pip install -r /requirements.txt
ENTRYPOINT ["jupyter"]
CMD ["notebook"]
