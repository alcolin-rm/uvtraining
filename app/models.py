from pydantic import BaseModel, Field, validator
from typing import Optional

ALLOWED_GENRES = [
    "horror", "adventure", "drama", "action",
    "comedy", "sci-fi", "fantasy", "thriller",
    "romance", "western", "detective", "animation",
    "crime"
]

class FilmModel(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=255)
    likes: int = Field(..., ge=0)
    dislikes: int = Field(..., ge=0)
    publish_year: int
    genre: str

    @validator('publish_year')
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