#FROM rabbitmq:3.12-management-alpine

#COPY ./plugins/rabbit_api/mq/plugins/rabbitmq_delayed_message_exchange-3.12.0.ez
#/opt/rabbitmq/plugins
COPY ./conf/rabbitmq.conf /etc/rabbitmq/conf.d/10-defaults.conf
#ENV RABBITMQ_CONFIG_FILE ./etc/rabbitmq/conf.d/10-defaults.conf

#RUN apt-get update \
# && apt-get install -y jq curl unzip nano \
# && rabbitmq-plugins enable rabbitmq_delayed_message_exchange

WORKDIR /

# Use the official RabbitMQ image as the base image
FROM rabbitmq:3.12-management-alpine

# Expose the necessary ports
EXPOSE 5672 15672

# Copy the custom configuration file into the container
#COPY rabbitmq.conf /etc/rabbitmq/

# Set the environment variable to use the custom configuration file
ENV RABBITMQ_CONFIG_FILE=/etc/rabbitmq1/conf.d/10-defaults.conf

# Optionally, you can copy any other custom plugins or configuration files
# For example, if you have a custom enabled_plugins file:
# COPY enabled_plugins /etc/rabbitmq/

# Start the RabbitMQ server when the container starts
CMD ["rabbitmq-server"]
