insert_templates = """
insert into content.templates (id, event, instant_event, title, text)
values  (2, 'news', false, 'News', 'Предлагаем ознакомиться с подборкой фильмов, которые подходят именно вам: {films}'),
        (1, 'like', false, 'Like', 'Пользователю {user_name} понравился ваш комментарий');
    """
