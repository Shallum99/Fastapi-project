from fastapi.testclient import TestClient

import pytest
from jose import jwt

import schemas
from config import settings

from main import app

client = TestClient(app)


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['admin_email'], "password": test_user['admin_pass']})

    login_res = schemas.Token(**res.json())
    print(login_res)
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['admin_id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 201


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])

def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
