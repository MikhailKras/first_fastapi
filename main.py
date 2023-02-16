from fastapi import FastAPI
from faker import Faker

app = FastAPI(
    title='My first FastAPI app'
)
fake = Faker()
fake_users = []
for i in range(1, 4):
    fake_users.append({'id': i, 'role': fake.job().lower(), 'name': fake.name()})


@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.13},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 125, 'amount': 2.13},
]


@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users2 = []
for i in range(1, 4):
    fake_users2.append({'id': i, 'role': fake.job().lower(), 'name': fake.name()})


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}
