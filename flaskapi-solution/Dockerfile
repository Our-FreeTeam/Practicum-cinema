FROM python:3.10

WORKDIR /opt/flaskapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY create_partitioned_tables.sql create_partitioned_tables.sql

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir \
     && apt-get update \
     && apt-get install -y postgresql-client

COPY . .

RUN chmod +x /opt/flaskapi/entrypoint.sh

ENTRYPOINT ["/opt/flaskapi/entrypoint.sh"]