from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from task_broker import TaskBroker
from models import User,UserInDB, UserSignUP
from repository import UserRepository
from security.hash_manager import hash_password, verify_password
from security.token_manager import create_access_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

t_broker = TaskBroker()
user_repo = UserRepository()

def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    pass

@app.post('/signup')
async def signup(new_user: UserSignUP) -> dict:
    hashed_password = hash_password(new_user.password)
    data = new_user.model_dump(exclude={'password'})
    user = UserInDB(**data, hashed_password=hashed_password)
    user_repo.add_user(user)
    return {'message': 'User created successfully!'}

@app.post('/login')
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user = user_repo.get_user_auth_data(form.username)
    if not user or  not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect login or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    token = create_access_token(user.id)
    return {'access_token': token, 'token_type': 'bearer'}



@app.post('/question')
async def question(req_data: Annotated[str, Depends(get_user)]) -> str:
    return t_broker.add_task(req_data)

@app.get('/question/result/{task_id}')
async def answer(task_id: str) -> str|None:
    return t_broker.get_task(task_id)

#test endpoints
@app.get('/users/all')
async def all_users():
    return user_repo.get_all_users()