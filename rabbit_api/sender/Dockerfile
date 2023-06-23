FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY rabbit_api/sender/requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./rabbit_api/sender/src .

RUN python3 /app/utils/create_delayed_exchange.py

CMD ["python3", "sender.py"]
