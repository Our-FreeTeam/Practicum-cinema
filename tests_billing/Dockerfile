FROM python:3.10

WORKDIR /tests_billing

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /tests_billing/entrypoint.sh

ENTRYPOINT ["/tests_billing/entrypoint.sh"]