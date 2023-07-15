insert_templates = """
insert into content.templates (id, event, instant_event, title, text)
values  ('d4d533b5-52c2-45fe-9cf3-0b753fa4618b', 'news', false, 'News', 'Предлагаем ознакомиться с подборкой фильмов, которые подходят именно вам: {films}'),
        ('90e6b6d5-4ac0-4d33-b7a3-61d6f339b191', 'like', false, 'Like', 'Пользователю {user_name} понравился ваш комментарий'),
        ('e74608ce-9ce8-40cd-8083-28d7e3f6975f', 'watched_film', false, 'Watched film',
         'На этой неделе Вы посмотрели всего {films_count} фильмов. Предлагаем Вам отдохнуть за просмотром фильма :)');
    """
