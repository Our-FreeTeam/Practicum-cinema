FROM python:3.10

WORKDIR /opt/logs_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir \
     && apt-get update

COPY . .

ENTRYPOINT ["python", "main.py"]