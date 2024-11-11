from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

from pydantic import BaseModel

app = FastAPI()
users = []


class User(BaseModel):
    id: int
    name: str
    age: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def get_users() -> list[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=3, max_length=20)],
                      age: Annotated[int, Path(gt=18)]) -> User:
    users.append(User(id=(len(users) + 1), name=username, age=age))
    return users[len(users) - 1]


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(gt=0)],
                      username: Annotated[str, Path(min_length=3, max_length=20)],
                      age: Annotated[int, Path(gt=18)]) -> User:
    try:
        users[user_id - 1].name = username
        users[user_id - 1].age = age
        return users[user_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(gt=0)]) -> User:
    try:
        return users.pop(user_id - 1)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")