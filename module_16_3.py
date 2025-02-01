from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get('/users')
async def get_all_users() -> dict:
    return users

@app.post('/user/{username}/{age}')
async def create_user(username : Annotated[str,Path(min_length=3, max_length=20,description='Введите имя')]
                      , age : Annotated[int, Path(ge=18,le=100,description='Введите возраст')]) -> str:
    user_id = str(int(max(users, key=int))+1)
    user_description = f'Имя {username}, возраст: {age}'
    users[user_id] = user_description
    return f'User {user_id} is registered'

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id : str,
                      username: Annotated[str, Path(min_length=3, max_length=20, description='Введите имя')]
                      , age: Annotated[int, Path(ge=18, le=100, description='Введите возраст')]
                      ) -> str:
    user_description_update = f'Имя {username}, возраст: {age}'
    users[user_id] = user_description_update
    return f'The user {user_id} is updated'

@app.delete('/user/{user_id}')
async def delete_user(user_id : str) -> str:
    users.pop(user_id)
    return f'User {user_id} was deleted'