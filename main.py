from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int
users: List[User] = []

@app.get('/users')
async def get_all_users():
    return [user.dict() for user in users]

@app.post('/user/{username}/{age}')
async def create_user(username: str = Path(..., description="Имя пользователя", min_length=5, max_length=20),
    age: int = Path(..., description="Возраст пользователя", ge=18, le=120)):
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user.dict()

#
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id : int = Path(..., description="Ввести ID пользователя",  ge=1, le=100),
                      username: str = Path(..., description="Имя пользователя", min_length=5, max_length=20),
                      age: int = Path(..., description="Возраст пользователя", ge=18, le=120)
                      ):
    user_found = None
    for user in users:
        if user.id == user_id:
            user_found = user
            break
        else:
            raise HTTPException(status_code=404, detail="Пользователь с таким ID не найден")
    user_found.username = username
    user_found.age = age

    return user_found.dict()

print("Current users:", [user.dict() for user in users])



#
# @app.delete('/user/{user_id}')
# async def delete_user(user_id : str) -> str:
#     users.pop(user_id)
#     return f'User {user_id} was deleted'