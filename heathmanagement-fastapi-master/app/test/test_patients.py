from fastapi.testclient import TestClient

import schemas
from config import settings

from main import app

client = TestClient(app)

def test_create_patient(client):

    res = client.post(
    "/patient", json={
        "patient_adhar": "A34DFS",
        "patient_mobile": 59687944,
        "patient_name": "Shallum2",
        "patient_address": "Mumbai",
        "patient_id": 1
    })

    new_user = schemas.Patient(**res.json())
    assert new_user.patient_name == "Shallum2"
    assert res.status_code == 201


def test_get_all_patient(test_patients):


    res = client.get("/patient")

    def validate(post):
        return schemas.Patient(**post)

    posts_map = map(validate, res.json())
    posts_list = list(res.json())
    print(posts_list)
    assert len(res.json()) == len(test_patients)
    assert res.status_code == 200


def test_get_one_patient(test_patients):
    res = client.get(f"/patient/{test_patients[0].patient_id}")
    post = schemas.Patient(**res.json())

    assert post.patient_id == test_patients[0].patient_id
    assert post.patient_name == test_patients[0].patient_name


def test_get_one_patient_not_exist():
    res = client.get(f"/patient/88888")
    assert res.status_code == 404


def test_delete_patient_success(test_patients):
    res = client.delete(
        f"/patient/{test_patients[0].patient_id}")

    assert res.status_code == 204


def test_delete_patient_non_exist():
    res = client.delete(
        f"/patient/8000000")

    assert res.status_code == 404


def test_update_patient(test_patients):
    data = {
        "patient_adhar": "A34DFS",
        "patient_mobile": 59687944,
        "patient_name": "Shallum2",
        "patient_address": "Mumbai",
        "patient_id": 2
    }
    print(test_patients[1].patient_id)
    res = client.put(f"/patient/{test_patients[1].patient_id}", json=data)
    updated_post = schemas.Patient(**res.json())
    assert res.status_code == 200

    assert updated_post.patient_name == data['patient_name']
    assert updated_post.patient_adhar == data['patient_adhar']


def test_update_patient_non_exist(test_patients):
    data = {
        "patient_adhar": "A34DFS",
        "patient_mobile": 59687944,
        "patient_name": "Shallum2",
        "patient_address": "Mumbai",
        "patient_id": 2
    }

    res = client.put(
        f"/patient/8000000", json=data)

    assert res.status_code == 404