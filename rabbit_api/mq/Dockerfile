# Use the official RabbitMQ image as the base image
FROM rabbitmq:3.12-management-alpine

COPY ./plugins/rabbit_api/mq/plugins/rabbitmq_delayed_message_exchange-3.12.0.ez /opt/rabbitmq/plugins
COPY ./conf/rabbitmq.conf /etc/rabbitmq/conf.d/10-default-guest-user.conf

RUN apt-get update \
 && apt-get install -y jq curl unzip nano \
 && rabbitmq-plugins enable rabbitmq_delayed_message_exchange


# Start the RabbitMQ server when the container starts
CMD ["rabbitmq-server"]
