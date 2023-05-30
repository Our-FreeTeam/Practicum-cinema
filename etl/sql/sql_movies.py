sql = '''
  select * from (
      select f.id as uuid
           , f.rating                                                              imdb_rating
           , json_agg(distinct jsonb_build_object('uuid',g.id, 'name', g.name))                   genre
           , f.title
           , f.description
           , COALESCE (
               json_agg(
                   DISTINCT jsonb_build_object(
                       'person_role', pfw.role,
                       'person_id', p.id,
                       'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id is not null),
               '[]'
           ) as persons
           , greatest(max(f.updated_at), max(g.updated_at), max(p.updated_at)) modified
        from content.film_work f
        join content.genre_film_work gf on f.id = gf.film_work_id
        join content.genre g on gf.genre_id = g.id
        left join content.person_film_work pfw on f.id = pfw.film_work_id
        left join content.person p on pfw.person_id = p.id
      group by f.id
             , f.rating
             , f.title
             , f.description
      having greatest(max(f.updated_at), max(g.updated_at), max(p.updated_at)) >= %s
  ) t order by modified asc
'''
