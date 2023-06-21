FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY rabbit_api/src/requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./rabbit_api/src .

EXPOSE 8000

RUN chmod +x /app/run.sh

ENTRYPOINT ["/app/run.sh"]
