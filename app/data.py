from typing import List
from models import FilmModel

INITIAL_MOVIES = [
    {"id": 1, "title": "Project Hail Mary", "publish_year": 2026, "genre": "sci-fi", "likes": 0, "dislikes": 0},
    {"id": 2, "title": "The Matrix", "publish_year": 1999, "genre": "action", "likes": 0, "dislikes": 0},
    {"id": 3, "title": "Interstellar", "publish_year": 2014, "genre": "sci-fi", "likes": 0, "dislikes": 0},
    {"id": 4, "title": "The Dark Knight", "publish_year": 2008, "genre": "action", "likes": 0, "dislikes": 0},
    {"id": 5, "title": "Pulp Fiction", "publish_year": 1994, "genre": "crime", "likes": 0, "dislikes": 0},
    {"id": 6, "title": "Fight Club", "publish_year": 1999, "genre": "drama", "likes": 0, "dislikes": 0},
    {"id": 7, "title": "Once Upon a Time in Hollywood", "publish_year": 2019, "genre": "comedy", "likes": 0, "dislikes": 0},
    {"id": 8, "title": "Kill Bill: Volume 1", "publish_year": 2003, "genre": "action", "likes": 0, "dislikes": 0},
    {"id": 9, "title": "Inglourious Basterds", "publish_year": 2009, "genre": "drama", "likes": 0, "dislikes": 0},
    {"id": 10, "title": "Django Unchained", "publish_year": 2012, "genre": "western", "likes": 0, "dislikes": 0}
]