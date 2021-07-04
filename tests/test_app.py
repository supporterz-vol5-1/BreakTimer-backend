import sys
from pathlib import Path

import pytest
from sqlalchemy.sql import text

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))
import db
from app import app


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
    r = client.get("/")
    assert r.status_code == 404


def test_api_root(client):
    r = client.get("/api")
    assert r.status_code == 404


def test_post_data(client):
    r = client.post("/api/hackathon-vol5-1")
    assert r.status_code == 403

    r = client.post(
        "/api/hackathon-vol5-1", data={"body": {"filetype": "python", "work_time": 300}}
    )
    assert r.status_code == 403

    r = client.post(
        "/api/hackathon-vol5-1", json={"body": {"filetype": "python", "work_time": 300}}
    )
    assert r.status_code == 403

    # r = client.post(
    #     "/api/invalid-user", json={"body": {"filetype": "python", "work_time": 300}}
    # )
    # assert r.status_code == 404

    r = client.post(
        "/api/hackathon-vol5-1",
        json={
            "body": {
                "filetype": "python",
                "work_time": 300,
                "token": "56af743f9ff7a944bc57f26bb9b1605b",
            }
        },
    )
    assert r.status_code == 200


def test_get_user_data(client):
    r = client.get("/api/hackathon-vol5-1")
    assert r.status_code == 200

    d = r.json
    assert len(d) == 7


def test_get_invalid_user_data(client):
    r = client.get("/api/invalid-user")
    assert r.status_code == 404


def test_get_user_data_with_filetype(client):
    r = client.get("/api/hackathon-vol5-1/python")
    assert r.status_code == 200

    d = r.json
    assert len(d) == 7

    for dd in d:
        assert "ruby" not in dd.keys()
