from sqlalchemy import inspect
from movie import db

def convert_object_to_dict(obj):
  return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def convert_model_to_dict(rows):
  return [convert_object_to_dict(row) for row in rows]

def paging(page, num, data):
  prev_page = page - 1
  start = prev_page * num
  end = start + num
  if start >= len(data):
    return []
  if end >= len(data):
    end = len(data)
  
  data = data[start:end]
  return data

def movie_sort(movies_lst, strategy):
  for movie in movies_lst:
    if movie['rating_count'] == None:
        movie['rating'] = 0
    else:
        movie['rating'] = round(movie['total_rating'] / movie['rating_count'], 1)
  
  if strategy == 'descending':
    movies_lst.sort(key=lambda x:(x.get('rating', 0)), reverse=True)
  elif strategy == 'ascending':
    movies_lst.sort(key=lambda x:(x.get('rating', 0)))
  return movies_lst