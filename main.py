from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from faker import Faker
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI(
    title='My first FastAPI app'
)
fake = Faker()
fake_users = []
for i in range(1, 4):
    fake_users.append({
        'id': i,
        'role': fake.job().lower(),
        'name': fake.name(),
        'degree': [
            {
                'id': int(fake.iana_id()),
                'created_at': fake.date('%Y-%m-%dT%H:%M:%S'),
                'type_degree': 'expert',
            }
        ]
    })


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    response = [user for user in fake_users if user.get('id') == user_id]
    if not response:
        raise HTTPException(status_code=404, detail='User not found')
    return response


fake_users2 = []
for i in range(1, 4):
    fake_users2.append({'id': i, 'role': fake.job().lower(), 'name': fake.name()})


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.13},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 125, 'amount': 2.13},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=15)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
