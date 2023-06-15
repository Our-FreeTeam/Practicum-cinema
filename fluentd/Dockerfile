FROM fluent/fluentd:v1.12-debian-1
USER root
RUN ["gem", "install", "fluent-plugin-gelf-hs", "--no-document", "--version", "1.0.8"]
USER fluent
