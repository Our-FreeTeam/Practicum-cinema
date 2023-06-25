insert_templates = """
insert into content.templates (event, instant_event, title, text)
values  ('news', false, 'News', 'Предлагаем ознакомиться с подборкой фильмов, которые подходят именно вам: {films}'),
        ('like', false, 'Like', 'Пользователю {user_name} понравился ваш комментарий'),
        ('watched_film', false, 'Watched film',
         'На этой неделе Вы посмотрели всего {films_count} фильмов. Предлагаем Вам отдохнуть за просмотром фильма :)')
;
    """
