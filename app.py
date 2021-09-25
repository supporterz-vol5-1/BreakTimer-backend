import os
from datetime import date, datetime
from typing import Any, Dict, Optional, Tuple, Union

from flask import Flask, jsonify, request
from flask.wrappers import Response

import db

app = Flask(__name__)


@app.route("/api/register/<string:user_name>", methods=["GET"])
def register_user(user_name: str) -> Tuple[Response, int]:
    status = db.register_user(app.config["ENGINE"], avatar="", user_name=user_name)
    if status is None:
        return jsonify({"message": "This user name is used already."}), 412
    else:
        return (jsonify({"token": status}), 200)


@app.route("/apiv2/register", methods=["POST"])
def register_user() -> Tuple[Response, int]:
    if request.headers["Content-Type"] != "application/json":
        return jsonify({"message": "Invalid Content-Type"}, 400)

    d = request.json
    status = db.register_user(app.config["ENGINE"],
                              user_name=d["login"],
                              avatar=user["avatar_url"])
    if status is None:
        return jsonify({"message": "This user name is used already."}), 412
    return jsonify({"token": status}), 200


@app.route("/api/<string:user_name>", methods=["POST"])
@app.route("/apiv2/<string:user_name>", methods=["POST"])
def register_work_time(user_name: str) -> Tuple[Response, int]:
    post_data: Optional[Dict[str, Any]] = request.json
    if post_data is None:
        return jsonify({"message": "invalid"}), 403
    if "token" not in post_data["body"]:
        return jsonify({"message": "Must set 'token'"}), 403

    today = date.today()
    try:
        db.update(app.config["ENGINE"], user_name, post_data["body"], day=today)
    except db.UserNotFoundError:
        return jsonify({"message": "The user is not found."}), 404
    except db.InvalidTokenError:
        return jsonify({"message": "The token is invalid."}), 403
    return jsonify({}), 200


@app.route("/api/<string:user_name>", methods=["GET"])
def get_recent_week_data(user_name: str) -> Tuple[Response, int]:
    seven_days = db.get_recent_week(app.config["ENGINE"], user_name)
    if seven_days is None:
        return jsonify({"message": "The user is not found."}), 404
    return jsonify(seven_days), 200


@app.route("/api/<user_name>/<string:filetype>", methods=["GET"])
def get_recent_week_data_with_filetype(
    user_name: str,
    filetype: str,
) -> Tuple[Response, int]:
    seven_days = db.get_recent_week(app.config["ENGINE"], user_name)
    if seven_days is None:
        return jsonify({"message": "The user is not found."}), 404
    return jsonify([{filetype: d.get(filetype, 0)} for d in seven_days]), 200


@app.route("/apiv2/user/<string:user_name>", methods=["GET"])
def get_user_info() -> Tuple[Response, int]:
    # WIP
    # TODO その情報にアクセスできる人かどうかの判定をする
    # headerにtokenとか？
    user = db.get_user_info(app.config["ENGINE"], user_name=user_name)


@app.route("/api/start/<string:user_name>", methods=["POST"])
@app.route("/apiv2/start/<string:user_name>", methods=["POST"])
def start_written(user_name: str) -> Tuple[Response, int]:
    post_data = request.json
    if post_data is None:
        return jsonify({"message": "invalid"}), 403
    now = datetime.now()
    db.start_written(
        engine=app.config["ENGINE"],
        user_name=user_name,
        now=now,
        request_body=post_data,
    )
    return jsonify({}), 200


@app.route("/api/stop/<string:user_name>", methods=["POST"])
@app.route("/apiv2/stop/<string:user_name>", methods=["POST"])
def stop_written(user_name: str) -> Tuple[Response, int]:
    post_data: Optional[Dict[str, Any]] = request.json
    if post_data is None:
        return jsonify({"message": "invalid"}), 403
    now = datetime.now()
    db.stop_written(
        engine=app.config["ENGINE"],
        user_name=user_name,
        now=now,
        request_body=post_data,
    )
    return jsonify({}), 200


def initialize_config():
    app.config["DB_USERNAME"] = os.environ.get("DB_USERNAME", "")
    app.config["DB_PASSWORD"] = os.environ.get("DB_PASSWORD", "")
    app.config["DB_HOST"] = os.environ.get("DB_HOST", "")
    app.config["DB_PORT"] = os.environ.get("DB_PORT", 0)
    app.config["DB_NAME"] = os.environ.get("DB_NAME", "")

    return db.create_engine(
        dialect="postgresql",
        driver="psycopg2",
        password=app.config["DB_PASSWORD"],
        host=app.config["DB_HOST"],
        username=app.config["DB_USERNAME"],
        port=app.config["DB_PORT"],
        dbname=app.config["DB_NAME"],
    )


if __name__ == "__main__":
    # for run locally
    engine = db.create_engine(
        dialect="sqlite",
        password="",
        host="",
        username="",
        port="",
        dbname="sample.db",
        driver="",
    )
    app.config["ENGINE"] = engine
    db.initialize(app.config["ENGINE"])
    app.run(debug=True)
else:
    # for run by gunicorn
    app.config["ENGINE"] = initialize_config()
