from fastapi.testclient import TestClient

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from main import app
from config import settings
from database import get_db
from database import Base
from oauth2 import create_access_token
import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):

    user_data = {
    "admin_id":"2",
    "admin_name":"shallum1",
    "admin_pass":"shallum1",
    "admin_email":"shallum1@gmail.com",
    "bed_avail":"1",
    "doc_avail":"2",
    "nurse_avail":"3"
    }
    res = client.post("/admin", json=user_data)

    assert res.status_code == 201

    new_user = res.json()

    new_user['admin_pass'] = user_data['admin_pass']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['admin_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(session):
    posts_data = [
    {
        "admin_name": "shallum1",
        "admin_email": "shallum1@gmail.com",
        "admin_pass": "$2b$12$ol7wNrAdhwtit7kCE33nWOXkLPELwVLOIj.OdQMU/69RV5P11iilq",
        "doc_avail": 2,
        "bed_avail": 1,
        "admin_id": 1,
        "nurse_avail": 3
    },
    {
        "admin_name": "shallum1",
        "admin_email": "shallum1@gmail.com",
        "admin_pass": "$2b$12$8ho2tvvYQ7YohvqnCNh/AeD9DP/iM0Et4sjH26GAhdAaFUsM535oO",
        "doc_avail": 2,
        "bed_avail": 1,
        "admin_id": 2,
        "nurse_avail": 3
    },
    {
        "admin_name": "shallum1",
        "admin_email": "shallum1@gmail.com",
        "admin_pass": "$2b$12$wlkAaFkpLqX8yBonk7u20uljE4qE37PDGipZy4q6krDhvv2mQjZL.",
        "doc_avail": 2,
        "bed_avail": 1,
        "admin_id": 3,
        "nurse_avail": 3
    },
    {
        "admin_name": "shallum1",
        "admin_email": "shallum1@gmail.com",
        "admin_pass": "$2b$12$7GF0laihM7j/b67.kwnJCenAJ4N9HLGeX6Y69yFJYsMM3oyrKd5tm",
        "doc_avail": 2,
        "bed_avail": 1,
        "admin_id": 4,
        "nurse_avail": 3
    }
    ]

    def create_post_model(post):
        return models.Admin(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
  
    session.commit()

    posts = session.query(models.Admin).all()
    return posts

@pytest.fixture
def test_patients(session):
    posts_data = [
    {
        "patient_adhar": "A34DFS",
        "patient_mobile": 59687944,
        "patient_name": "Shallum2",
        "patient_address": "Mumbai",
        "patient_id": 1
    },
    {
        "patient_adhar": "A34DFS",
        "patient_mobile": 59687944,
        "patient_name": "Shallum2",
        "patient_address": "Mumbai",
        "patient_id": 2
    }

]

    def create_post_model(post):
        return models.Patient(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
  
    session.commit()
    
    posts = session.query(models.Patient).all()
    return posts
