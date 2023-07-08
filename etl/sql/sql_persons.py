sql = """
    select p.id as uuid,
           p.full_name,
           p.updated_at as modified,
           json_agg(
               DISTINCT jsonb_build_object(
                   'roles', pfw.role,
                   'uuid', pfw.film_work_id
               )
           ) as films
      from content.person p
      left join content.person_film_work pfw on p.id = pfw.user_id
     where updated_at >= %s
    group by p.id, p.full_name, p.updated_at
    order by updated_at asc;
"""
