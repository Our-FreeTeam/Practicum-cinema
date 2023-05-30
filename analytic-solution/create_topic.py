import json
import logging

import requests
from settings import settings


def create_topic(topic_name: str):
    # Get cluster
    cluster_url = f'{settings.kafka_interface_url}/2.0/clusters/kafka/display/cluster_management'
    cluster_response = requests.get(cluster_url, timeout=settings.request_timeout)
    cluster_id = cluster_response.json()["defaultClusterId"]

    # Create topic
    topic_url = f'{settings.kafka_interface_url}/2.0/kafka/{cluster_id}/topics?validate=false'
    headers = {"Content-Type": "application/json"}
    # Default settings
    topic_settings = {
        "name": topic_name,
        "numPartitions": "6",
        "replicationFactor": "1",
        "configs": {
            "compression.type": "producer",
            "confluent.tier.cleaner.compact.min.efficiency": "0.5",
            "confluent.value.schema.validation": "false",
            "leader.replication.throttled.replicas": "",
            "confluent.key.subject.name.strategy": "io.confluent.kafka.serializers.subject.TopicNameStrategy",
            "min.insync.replicas": "1",
            "message.downconversion.enable": "true",
            "segment.jitter.ms": "0",
            "confluent.tier.cleaner.enable": "false",
            "cleanup.policy": "delete",
            "confluent.compacted.topic.prefer.tier.fetch.ms": "-1",
            "flush.ms": "9223372036854775807",
            "confluent.tier.local.hotset.ms": "86400000",
            "follower.replication.throttled.replicas": "",
            "confluent.value.subject.name.strategy": "io.confluent.kafka.serializers.subject.TopicNameStrategy",
            "confluent.tier.local.hotset.bytes": "-1",
            "segment.bytes": "1073741824",
            "retention.ms": "604800000",
            "flush.messages": "9223372036854775807",
            "confluent.tier.enable": "false",
            "confluent.tier.segment.hotset.roll.min.bytes": "104857600",
            "confluent.segment.speculative.prefetch.enable": "false",
            "message.format.version": "3.0-IV1",
            "file.delete.delay.ms": "60000",
            "confluent.tier.cleaner.compact.segment.min.bytes": "20971520",
            "max.compaction.lag.ms": "9223372036854775807",
            "confluent.tier.cleaner.dual.compaction": "false",
            "max.message.bytes": "1048588",
            "min.compaction.lag.ms": "0",
            "message.timestamp.type": "CreateTime",
            "preallocate": "false",
            "min.cleanable.dirty.ratio": "0.5",
            "index.interval.bytes": "4096",
            "unclean.leader.election.enable": "false",
            "delete.retention.ms": "86400000",
            "retention.bytes": "-1",
            "confluent.tier.cleaner.min.cleanable.ratio": "0.75",
            "confluent.prefer.tier.fetch.ms": "-1",
            "confluent.key.schema.validation": "false",
            "segment.ms": "604800000",
            "message.timestamp.difference.max.ms": "9223372036854775807",
            "segment.index.bytes": "10485760",
        },
    }
    topic_settings = json.dumps(topic_settings)
    requests.put(topic_url, data=topic_settings, headers=headers, timeout=settings.request_timeout)

    return True


logging.basicConfig(format=settings.log_format, level=settings.log_level)
create_topic(settings.topic_name)
