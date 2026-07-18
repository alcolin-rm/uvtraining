from fastapi import FastAPI

app = FastAPI(title="User API", version="1.0.0")

USERS = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

@app.get("/")
def root():
    return {"message": "sup"}

@app.get("/users")
def get_users():

    return USERS

@app.get("/users_count")
def get_users_count():

    return {"count": len(USERS)}
