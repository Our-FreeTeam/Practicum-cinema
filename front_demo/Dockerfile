FROM python:3.10

WORKDIR /opt/fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .


CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "9000"]