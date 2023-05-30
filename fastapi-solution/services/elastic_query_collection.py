# Elastic body queries for different cases

# This is base query for select list of movies with filters : genre.uuid, person.uuid and query
# base sceleton with %s for prep_genre_query, prep_person_query and other for prep_text_query
# BASE
prep_full_query = '''
{
  "query": {
    "bool": {
      %s
    }
  }%s
}'''

# GENRE QUERY
prep_genre_query = '''
      "filter": {
        "nested": {
          "path": "genre",
          "query": {
            "term": {
              "genre.uuid": "%s"
            }
          }
        }
      }
'''

# FILM QUERY FOR PERSONS
prep_film_person_query = '''
{
  "query": {
    "bool": {
      "filter": {
        "terms": {
          "uuid": %s
        }
      }
    }
  }
}
'''

# Полнотекстовый поиск
prep_text_query = '''
      "must": {
        "multi_match": {
          "fields": [%s],
          "query": "%s",
          "operator": "and"
        }
      }
'''

# Скроллинг с использованием search_after
prep_search_after_query = ''' ,
  "search_after": ["%s"]
'''

# Заготовка для "похожих фильмов"
more_like_this_query = '''
{
  "query": {
    "more_like_this" : {
      "fields" : ["title", "description"],
      "like" : "Once upon a time",
      "min_term_freq" : 1,
      "max_query_terms" : 12
    }
  }
}
'''
