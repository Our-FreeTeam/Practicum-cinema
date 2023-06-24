FROM python:3.10

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY crontab /etc/cron.d/crontab

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir\
     && apt-get update \
     && apt-get -y install cron busybox locales

COPY . .

ENTRYPOINT ["python","/opt/utils/email_to_queue.py"]

#RUN crontab /etc/cron.d/crontab

#ENTRYPOINT ["/opt/app/run.sh"]
