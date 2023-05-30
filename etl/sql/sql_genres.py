sql = """
    SELECT id as uuid, name, description, updated_at AS modified
      FROM content.genre
     WHERE updated_at >= %s
    ORDER BY updated_at ASC;
"""
