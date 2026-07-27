from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

ALLOWED_GENRES = [
    "horror", "adventure", "drama", "action",
    "comedy", "sci-fi", "fantasy", "thriller",
    "romance", "western", "detective", "animation"
]

class FilmModel(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=255)
    likes: int = Field(..., ge=0)
    dislikes: int = Field(..., ge=0)
    publish_year: int
    genre: str

    @validator('publish_year') #cant get around it tbh
    def validate_publish_year(cls, v):
        if v < 1888:
            raise ValueError('publish_year must be at least 1888')
        return v

    @validator('genre')
    def validate_genre(cls, v):
        if v not in ALLOWED_GENRES:
            raise ValueError(f'genre must be one of: {", ".join(ALLOWED_GENRES)}')
        return v

    @validator('title')
    def validate_title(cls, v):
        if not v or v.isspace():
            raise ValueError('title cannot be empty or contain only spaces')
        return v.strip()

class FilmUpdateModel(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    likes: Optional[int] = Field(None, ge=0)
    dislikes: Optional[int] = Field(None, ge=0)
    publish_year: Optional[int] = None
    genre: Optional[str] = None

    @validator('publish_year')
    def validate_publish_year(cls, v):
        if v is not None and v < 1888:
            raise ValueError('publish_year must be at least 1888')
        return v

    @validator('genre')
    def validate_genre(cls, v):
        if v is not None and v not in ALLOWED_GENRES:
            raise ValueError(f'genre must be one of: {", ".join(ALLOWED_GENRES)}')
        return v

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if not v or v.isspace():
                raise ValueError('title cannot be empty or contain only spaces')
            return v.strip()
        return v

films_db: List[FilmModel] = []
film_id_counter = 1

@app.get("/films", response_model=List[FilmModel])
async def get_films():
    return films_db

@app.get("/film/{film_id}", response_model=FilmModel)
async def get_film(film_id: int):
    for film in films_db:
        if film.id == film_id:
            return film
    raise HTTPException(status_code=404, detail="Film not found")

@app.post("/film", response_model=FilmModel, status_code=201)
async def create_film(film: FilmModel):
    global film_id_counter
    #taranino could never
    for existing_film in films_db:
        if existing_film.id == film.id:
            raise HTTPException(
                status_code=400, 
                detail=f"Film with id {film.id} already exists"
            )
    
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
async def update_film(film_id: int, updated_film: FilmUpdateModel):
    for index, existing_film in enumerate(films_db):
        if existing_film.id == film_id:
            update_data = updated_film.dict(exclude_unset=True)
            
            updated_film_obj = FilmModel(
                id=film_id,
                title=update_data.get('title', existing_film.title),
                likes=update_data.get('likes', existing_film.likes),
                dislikes=update_data.get('dislikes', existing_film.dislikes),
                publish_year=update_data.get('publish_year', existing_film.publish_year),
                genre=update_data.get('genre', existing_film.genre),
            )
            films_db[index] = updated_film_obj
            return updated_film_obj
    
    raise HTTPException(status_code=404, detail="film not found")

@app.delete("/film/{film_id}", status_code=204)
async def delete_film(film_id: int):
    for index, film in enumerate(films_db):
        if film.id == film_id:
            films_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="film not found")