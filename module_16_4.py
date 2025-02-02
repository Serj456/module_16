from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int
users: List[User] = [
    User(id=1,username="Sergogo",age=22)]

@app.get('/users', response_model=List[User])
async def get_all_users():
    return users

class User_Create(BaseModel):
    username: str = Field(..., min_length=5,max_length=25, description='Введите имя пользователя')
    age: int

@app.post('/user/{username}/{age}', response_model=User)
async def create_user(user:User_Create):
    new_id = max((u.id for u in users), default=0)+1
    new_user = User(id=new_id,username = user.username, age = user.age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id : int, user : User_Create):
    for u in users:
        if u.id == user_id:
            u.username = user.username
            u.age = user.age
            return u
    raise HTTPException(status_code=404, detail="Пользователь с таким ID не найден")

@app.delete('/user/{user_id}', response_model=dict)
async def delete_user(user_id : int):
    for i,t in enumerate(users):
        if t.id == user_id:
            del users[i]
            return {'detail':'Юзер удален'}
    raise HTTPException(status_code=404, detail="Пользователь с таким ID не найден")
