FROM python:3.10

WORKDIR /opt/fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x entrypoint.sh

CMD ["/opt/fastapi/entrypoint.sh"]