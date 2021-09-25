import sys
from pathlib import Path

import pytest
from sqlalchemy.sql import text

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))
import db
from app import app

USERNAME = "hackathon-vol5-1"
TOKEN = "56af743f9ff7a944bc57f26bb9b1605b"
INVALID_USERNAME = "INVALID"
INVALID_TOKEN = "INVALID"
NON_ACTIVE_USER = "non-active"


@pytest.fixture()
def client():
    engine = db.create_engine(
        dialect="sqlite",
        password="",
        host="",
        username="",
        port="",
        dbname=str(project_dir / "testdb.db"),
        driver="",
    )
    app.config["ENGINE"] = engine
    db.initialize(app.config["ENGINE"])

    ses = db.create_session(app.config["ENGINE"])
    with open(project_dir / "sample.sql") as f:
        for line in f.readlines():
            t = text(line)
            ses.execute(t)
    ses.commit()

    # app.run(port=8080)
    client = app.test_client()

    yield client


def test_get_root(client):
    """User should not access root"""

    r = client.get("/")
    assert r.status_code == 404


def test_api_root(client):
    """User should not access api without username"""
    r = client.get("/api")
    assert r.status_code == 404


def test_post_data_without_body(client):
    """User should not post without body"""
    r = client.post("/api/hackathon-vol5-1")
    assert r.status_code == 403


def test_post_data_must_be_json(client):
    """Post data must be json"""
    r = client.post(
        f"/api/{USERNAME}",
        data={
            "body": {
                "filetype": "python",
                "work_time": 300,
                "token": TOKEN,
            }
        },
    )
    assert r.status_code == 403

    r = client.post(
        f"/api/{USERNAME}",
        json={
            "body": {
                "filetype": "python",
                "work_time": 300,
                "token": TOKEN,
            }
        },
    )
    assert r.status_code == 200


@pytest.mark.freeze_time("2000-01-01 12:00:00")
def test_start_writing(client):
    """User can register start time"""
    # request must has json
    r = client.post(f"/api/start/{USERNAME}", data={"body": "invalid"})
    assert r.status_code == 403

    # user must be exist
    r = client.post(
        f"/api/start/{INVALID_USERNAME}",
        json={"body": {"filetype": "python", "token": INVALID_TOKEN}},
    )
    assert r.status_code == 404

    # must has valid token
    r = client.post(
        f"/api/start/{USERNAME}",
        json={"body": {"filetype": "python", "token": INVALID_TOKEN}},
    )
    assert r.status_code == 403

    # valid request
    r = client.post(
        f"/api/start/{USERNAME}",
        json={
            "body": {
                "filetype": "python",
                "token": TOKEN,
            }
        },
    )
    assert r.status_code == 200
    # dbに本当に入ってるかテストしたい


@pytest.mark.freeze_time("2000-01-01 12:00:00")
def test_stop_writing(client):
    """User can register stop time"""
    # request must has json
    r = client.post(f"/api/stop/{USERNAME}", data={"body": "invalid"})
    assert r.status_code == 403

    # user must be exist
    r = client.post(
        f"/api/stop/{INVALID_USERNAME}",
        json={
            "body": {"filetype": "python", "token": INVALID_TOKEN},
        },
    )
    assert r.status_code == 404

    # must has valid token
    r = client.post(
        f"/api/stop/{USERNAME}",
        json={"body": {"filetype": "python", "token": INVALID_TOKEN}},
    )
    assert r.status_code == 403

    # valid request
    r = client.post(
        f"/api/stop/{USERNAME}",
        json={
            "body": {
                "filetype": "python",
                "token": TOKEN,
            }
        },
    )
    assert r.status_code == 200
    # dbに本当に入ってるかテストしたい


def test_post_data_without_token(client):
    """User should not post without token"""
    r = client.post(
        f"/api/{USERNAME}", data={"body": {"filetype": "python", "work_time": 300}}
    )
    assert r.status_code == 403

    r = client.post(
        f"/api/{USERNAME}", json={"body": {"filetype": "python", "work_time": 300}}
    )
    assert r.status_code == 403

    # r = client.post(
    #     "/api/invalid-user", json={"body": {"filetype": "python", "work_time": 300}}
    # )
    # assert r.status_code == 404


@pytest.mark.freeze_time("2021-07-04 12:00:00")
def test_get_user_data(client):
    """User can get information via GET method"""
    r = client.get(f"/api/{USERNAME}")
    assert r.status_code == 200

    d = r.json
    assert len(d) == 7

    for dd in d:
        assert bool(dd)  # this user is fully active


def test_get_invalid_user_data(client):
    """User should not access unexisted user"""
    r = client.get(f"/api/{INVALID_USERNAME}")
    assert r.status_code == 404


def test_get_non_active_user_info(client):
    """User can get non active user's information"""
    r = client.get(f"/api/{NON_ACTIVE_USER}")
    for d in r.json:
        assert not bool(d)  # if dict is empty, bool({}) will is False.


def test_get_user_data_with_filetype(client):
    """User can get information with specifying language"""
    r = client.get(f"/api/{USERNAME}/python")
    assert r.status_code == 200

    d = r.json
    assert len(d) == 7

    for dd in d:
        assert "ruby" not in dd.keys()
