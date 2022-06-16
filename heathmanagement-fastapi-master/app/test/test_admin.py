from fastapi.testclient import TestClient

from config import settings
from main import app
import schemas


client = TestClient(app)

def test_create_user(client):

    res = client.post(
    "/admin", json={
    "admin_id":"1",
    "admin_name":"shallum1",
    "admin_pass":"shallum1",
    "admin_email":"shallum1@gmail.com",
    "bed_avail":"1",
    "doc_avail":"2",
    "nurse_avail":"3"
    })

    new_user = schemas.Admin(**res.json())
    assert new_user.admin_email == "shallum1@gmail.com"
    assert res.status_code == 201


def test_get_all_admin(test_posts):

    res = client.get("/admin")

    def validate(post):
        return schemas.Admin(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_one_admin(test_posts):
    res = client.get(f"/admin/{test_posts[0].admin_id}")
    post = schemas.Admin(**res.json())

    assert post.admin_id == test_posts[0].admin_id
    assert post.admin_name == test_posts[0].admin_name
    assert post.admin_pass == test_posts[0].admin_pass
    assert post.admin_email == test_posts[0].admin_email
    assert post.bed_avail == test_posts[0].bed_avail
    assert post.nurse_avail == test_posts[0].nurse_avail


def test_get_one_admin_not_exist():
    res = client.get(f"/admin/88888")
    assert res.status_code == 404


def test_delete_admin_success(test_posts):
    res = client.delete(
        f"/admin/{test_posts[0].admin_id}")

    assert res.status_code == 204


def test_delete_admin_non_exist():
    res = client.delete(
        f"/admin/8000000")

    assert res.status_code == 404


def test_update_admin(test_posts):
    data = {
    "admin_id":"2",
    "admin_name":"shallum1",
    "admin_pass":"shallum2",
    "admin_email":"shallum1@gmail.com",
    "bed_avail":"1",
    "doc_avail":"2",
    "nurse_avail":"3"
    }

    res = client.put(f"/admin/{test_posts[1].admin_id}", json=data)
    updated_post = schemas.Admin(**res.json())
    assert res.status_code == 200

    assert updated_post.admin_pass == data['admin_pass']
    assert updated_post.admin_email == data['admin_email']


def test_update_admin_non_exist(test_posts):
    data = {
    "admin_id":"2",
    "admin_name":"shallum1",
    "admin_pass":"shallum2",
    "admin_email":"shallum1@gmail.com",
    "bed_avail":"1",
    "doc_avail":"2",
    "nurse_avail":"3"
    }
    
    res = client.put(
        f"/admin/8000000", json=data)

    assert res.status_code == 404