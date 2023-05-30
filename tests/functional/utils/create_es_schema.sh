echo "====== CREATE FILMS INDEX ======"

curl -XPUT ${ELASTIC_URL}/films -H 'Content-Type: application/json' -d'
{
  "settings": {
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      },
      "analyzer": {
        "ru_en": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "english_stemmer",
            "english_possessive_stemmer",
            "russian_stop",
            "russian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "uuid": {
        "type": "keyword"
      },
      "imdb_rating": {
        "type": "float"
      },
      "genre": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "title": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "director": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "actors_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "writers_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "actors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "writers": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      }
    }
  }
}'

echo "====== CREATE GENRES INDEX ======"

curl -XPUT ${ELASTIC_URL}/genres -H 'Content-Type: application/json' -d'
{
  "settings": {
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      },
      "analyzer": {
        "ru_en": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "english_stemmer",
            "english_possessive_stemmer",
            "russian_stop",
            "russian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "uuid": {
        "type": "keyword"
      },
      "name": {
        "type": "keyword"
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      }
    }
  }
}'


echo "====== CREATE PERSONS INDEX ======"

curl -XPUT ${ELASTIC_URL}/persons -H 'Content-Type: application/json' -d'
{
  "settings": {
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      },
      "analyzer": {
        "ru_en": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "english_stemmer",
            "english_possessive_stemmer",
            "russian_stop",
            "russian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "uuid": {
        "type": "keyword"
      },
      "full_name": {
        "type":  "text",
        "analyzer": "ru_en"
      },
      "films": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "roles": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      }
    }
  }
}'


echo "====== CREATE 3 LAST_MODIFIED INDEXes ======"

curl -XPUT ${ELASTIC_URL}/last_modified_genres -H 'Content-Type: application/json' -d'
{  "mappings": {
    "dynamic": "strict",
    "properties": {
      "last_modified": {
        "type": "date"
      },
      "try_count": {
        "type": "short"
      }
    }
}
}'

curl -XPUT ${ELASTIC_URL}/last_modified_persons -H 'Content-Type: application/json' -d'
{  "mappings": {
    "dynamic": "strict",
    "properties": {
      "last_modified": {
        "type": "date"
      },
      "try_count": {
        "type": "short"
      }
    }
}
}'

curl -XPUT ${ELASTIC_URL}/last_modified_films -H 'Content-Type: application/json' -d'
{  "mappings": {
    "dynamic": "strict",
    "properties": {
      "last_modified": {
        "type": "date"
      },
      "try_count": {
        "type": "short"
      }
    }
}
}'