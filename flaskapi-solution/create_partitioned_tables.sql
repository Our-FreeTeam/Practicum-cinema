\set ON_ERROR_STOP on


do $$
declare
  p_count integer;
begin

  SELECT count(*) AS partitions
    into p_count
    FROM   pg_catalog.pg_inherits
   WHERE  inhparent = 'event_entity'::regclass;

  if (p_count > 0) then
     raise exception 'Table is already partitioned!';
  end if;
end $$;

create table event_entity_partitioned
(
    id           varchar(36) not null,
    client_id    varchar(255),
    details_json varchar(2550),
    error        varchar(255),
    ip_address   varchar(255),
    realm_id     varchar(255),
    session_id   varchar(255),
    event_time   bigint,
    type         varchar(255),
    user_id      varchar(255),
    primary key (id, event_time)
)
partition by range(event_time);

alter table event_entity_partitioned
    owner to postgres;

create index idx_event_time_partitioned
    on event_entity_partitioned (realm_id, event_time);

DO $$
DECLARE
  start_date DATE := '2023-04-01';
  end_date DATE := '2024-04-01';
  curr_date DATE := start_date;
  table_prefix VARCHAR := 'event_entity_partitioned';
  res_str varchar;
BEGIN
  WHILE curr_date <= end_date LOOP
    -- Do something with the current date
    res_str := 'create table '||table_prefix||'_'||to_char(curr_date, 'yymm')||
      ' partition of '||table_prefix||' for values from (extract(epoch from timestamp '''||
      curr_date||''') * 1000) to (extract(epoch from timestamp '''||
      curr_date + INTERVAL '1 MONTH'||''') * 1000)';
    execute res_str;
    curr_date := curr_date + INTERVAL '1 MONTH';
  END LOOP;
END $$;


INSERT INTO event_entity_partitioned
    (id, client_id, details_json, error, ip_address, realm_id, session_id, event_time, type, user_id)
SELECT id, client_id, details_json, error, ip_address, realm_id, session_id, event_time, type, user_id
from event_entity;

drop table event_entity;

alter table event_entity_partitioned rename to event_entity;
