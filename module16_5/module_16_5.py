from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int
    name: str
    age: int


@app.get("/")
async def new_response(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(request: Request,
                   user_id: Annotated[int, Path(gt=0)]) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})


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
