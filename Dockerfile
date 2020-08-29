FROM python:3.7
RUN pip install kopf
RUN pip install kubernetes
RUN mkdir /src
ADD py-kopf.py /src
ADD task-template.yaml /src
CMD kopf run --standalone /src/py-kopf.py --verbose