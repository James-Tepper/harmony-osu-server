FROM python:3.11

ENV PYTHONBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt update && \
    apt install -y postgresql-client


COPY scripts /scripts
RUN chmod u+x /scripts/*

COPY . /srv/root
WORKDIR /srv/root

EXPOSE 80

# ENTRYPOINT [ "/scripts/bootstrap.sh" ]
