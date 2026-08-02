from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import List
from models import FilmModel, FilmUpdateModel
from data import INITIAL_MOVIES
from jinja2 import Environment, FileSystemLoader

app = FastAPI(
    title="Film Management API",
    description="API for managing film database with admin dashboard",
    version="1.0.0"
)

# custom template rendering to avoid jinja2 cache issue
template_env = Environment(loader=FileSystemLoader("templates"))
template_env.cache = {}

def render_template(template_name: str, context: dict):
    template = template_env.get_template(template_name)
    return HTMLResponse(content=template.render(**context))

films_db: List[FilmModel] = []
film_id_counter = 11

for movie in INITIAL_MOVIES:
    films_db.append(FilmModel(**movie))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    root endpoint - displays the admin dashboard with film statistics.
    
    returns:
        htmlresponse: rendered admin dashboard page
    """
    total_count = len(films_db)
    most_liked = max(films_db, key=lambda x: x.likes) if films_db else None
    most_disliked = max(films_db, key=lambda x: x.dislikes) if films_db else None
    
    return render_template(
        "index.html",
        {
            "request": request,
            "total_count": total_count,
            "most_liked": most_liked,
            "most_disliked": most_disliked,
            "films": films_db
        }
    )


@app.get("/api/films", response_model=List[FilmModel])
async def get_films():
    """
    retrieve all films from the database.
    
    returns:
        list[filmmodel]: list of all films
    """
    return films_db


@app.get("/api/film/{film_id}", response_model=FilmModel)
async def get_film(film_id: int):
    """
    retrieve a specific film by id.
    
    args:
        film_id (int): the id of the film to retrieve
        
    returns:
        filmmodel: the requested film
        
    raises:
        httpexception: 404 if film not found
    """
    for film in films_db:
        if film.id == film_id:
            return film
    raise HTTPException(status_code=404, detail="Film not found")


@app.post("/api/film", response_model=FilmModel, status_code=201)
async def create_film(film: FilmModel):
    """
    create a new film in the database.
    
    args:
        film (filmmodel): the film data to create
        
    returns:
        filmmodel: the created film with auto-generated id
        
    raises:
        httpexception: 400 if id already exists
    """
    global film_id_counter
    
    for existing in films_db:
        if existing.id == film.id:
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


@app.patch("/api/film/{film_id}", response_model=FilmModel)
async def update_film(film_id: int, updated: FilmUpdateModel):
    """
    update an existing film.
    
    args:
        film_id (int): the id of the film to update
        updated (filmupdatemodel): the fields to update
        
    returns:
        filmmodel: the updated film
        
    raises:
        httpexception: 404 if film not found
    """
    for idx, film in enumerate(films_db):
        if film.id == film_id:
            data = updated.dict(exclude_unset=True)
            
            updated_film = FilmModel(
                id=film_id,
                title=data.get('title', film.title),
                likes=data.get('likes', film.likes),
                dislikes=data.get('dislikes', film.dislikes),
                publish_year=data.get('publish_year', film.publish_year),
                genre=data.get('genre', film.genre),
            )
            films_db[idx] = updated_film
            return updated_film
    
    raise HTTPException(status_code=404, detail="Film not found")


@app.delete("/api/film/{film_id}", status_code=204)
async def delete_film(film_id: int):
    """
    delete a film by id.
    
    args:
        film_id (int): the id of the film to delete
        
    returns:
        none: returns 204 no content on success
        
    raises:
        httpexception: 404 if film not found
    """
    for idx, film in enumerate(films_db):
        if film.id == film_id:
            films_db.pop(idx)
            return
    
    raise HTTPException(status_code=404, detail="Film not found")