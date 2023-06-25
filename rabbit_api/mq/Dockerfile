# Use the official RabbitMQ image as the base image
FROM rabbitmq:3.12-management

COPY ./plugins /opt/rabbitmq/plugins
COPY ./conf/rabbitmq.conf /etc/rabbitmq/conf.d/10-default-guest-user.conf

RUN rabbitmq-plugins enable rabbitmq_delayed_message_exchange


## Start the RabbitMQ server when the container starts
CMD ["rabbitmq-server"]
