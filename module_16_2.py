from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def main_page() -> dict:
    return {"message": "Главная страница"}


@app.get("/user/admin")
async def admin_page() -> dict:
    return {"message": "Вы вошли как администратор"}


@app.get("/user/{user_id}")
async def user_page(user_id: Annotated[int, Path(ge=1, le=100, strict=True, description="Enter User ID", example=1)]) -> dict:
    return {"message": f"Вы вошли как пользователь №{user_id}"}


@app.get("/user/{username}/{age}")
async def user_page(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter Username", example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, strict=True, description="Enter Age", example=24)]) -> dict:
    return {"message": f"Вы вошли как пользователь {username} с возрастом {age}"}
