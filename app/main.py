from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class FilmModel(BaseModel):
    id: int
    title: str
    likes: int
    dislikes: int
    publish_year: int
    genre: str

films_db: List[FilmModel] = []
film_id_counter = 1 


@app.get("/films", response_model=List[FilmModel])
async def get_films():
    """return list."""
    return films_db

@app.get("/film/{film_id}", response_model=FilmModel)
async def get_film(film_id: int):
    """return film by id."""
    for film in films_db:
        if film.id == film_id:
            return film
    raise HTTPException(status_code=404, detail="film not found.")

@app.post("/film", response_model=FilmModel, status_code=201)
async def create_film(film: FilmModel):
    """
    new film. tarantino could never.
    """
    global film_id_counter
    new_film = FilmModel(
        id=film_id_counter,
        title=film.title,
        likes=film.likes,
        dislikes=film.dislikes,
        publish_year=film.publish_year,
        genre=film.genre,
    )
    films_db.append(new_film)
    film_id_counter += 1
    return new_film

@app.patch("/film/{film_id}", response_model=FilmModel)
async def update_film(film_id: int, updated_film: FilmModel):
    """
    update film.
    """
    for index, existing_film in enumerate(films_db):
        if existing_film.id == film_id:
            updated_film_with_id = FilmModel(
                id=film_id,
                title=updated_film.title,
                likes=updated_film.likes,
                dislikes=updated_film.dislikes,
                publish_year=updated_film.publish_year,
                genre=updated_film.genre,
            )
            films_db[index] = updated_film_with_id
            return updated_film_with_id
    raise HTTPException(status_code=404, detail="Film not found")

@app.delete("/film/{film_id}", status_code=204)
async def delete_film(film_id: int):
    """delete a film by id."""
    for index, film in enumerate(films_db):
        if film.id == film_id:
            films_db.pop(index)
            return  # (204)
    raise HTTPException(status_code=404, detail="Film not found")