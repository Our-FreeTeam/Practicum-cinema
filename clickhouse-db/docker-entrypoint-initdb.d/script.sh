#!/bin/bash

execute_shard() {
  shard_name=$1
  replica_name=$2

  clickhouse-client --query "CREATE DATABASE IF NOT EXISTS shard;"
  clickhouse-client --query "CREATE TABLE IF NOT EXISTS shard.views (id String, film_frame Int32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/$shard_name/views', '$replica_name') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;"
  clickhouse-client --query "CREATE TABLE IF NOT EXISTS default.views (id String, film_frame Int32, event_time DateTime) ENGINE = Distributed('company_cluster', '', views, rand());"
}

execute_replica() {
  shard_name=$1
  replica_name=$2

  clickhouse-client --query "CREATE DATABASE IF NOT EXISTS replica;"
  clickhouse-client --query "CREATE TABLE IF NOT EXISTS replica.views (id String, film_frame Int32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/$shard_name/views', '$replica_name') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;"
}

execute_mat_view() {
  db_name=$1

  echo $KAFKA_BROKER_URL
  clickhouse-client --query "CREATE TABLE IF NOT EXISTS $db_name.views_queue on cluster company_cluster (id String, film_frame Int32, event_time DateTime) ENGINE = Kafka SETTINGS kafka_broker_list = '$KAFKA_BROKER_URL', kafka_topic_list = 'views', kafka_group_name = 'views_clickhouse_group', kafka_format = 'CSV', kafka_max_block_size = 1048576;"
  clickhouse-client --query "CREATE MATERIALIZED VIEW IF NOT EXISTS $db_name.views_queue_mv on cluster company_cluster TO $db_name.views AS SELECT id, film_frame, event_time FROM $db_name.views_queue;"
}


if [ "$HOSTNAME" = "clickhouse-node1" ]; then
  execute_shard "shard1" "replica_1" && execute_mat_view "shard"
elif [ "$HOSTNAME" = "clickhouse-node2" ]; then
  execute_replica "shard1" "replica_2"
elif [ "$HOSTNAME" = "clickhouse-node3" ]; then
  execute_replica "shard1" "replica_3"
elif [ "$HOSTNAME" = "clickhouse-node4" ]; then
  execute_shard "shard2" "replica_1"
elif [ "$HOSTNAME" = "clickhouse-node5" ]; then
  execute_replica "shard2" "replica_2"
elif [ "$HOSTNAME" = "clickhouse-node6" ]; then
  execute_replica "shard2" "replica_3"
elif [ "$HOSTNAME" = "clickhouse-node7" ]; then
  execute_shard "shard3" "replica_1"
elif [ "$HOSTNAME" = "clickhouse-node8" ]; then
  execute_replica "shard3" "replica_2"
elif [ "$HOSTNAME" = "clickhouse-node9" ]; then
  execute_replica "shard3" "replica_3"
fi
