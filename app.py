import os
from datetime import date

from flask import Flask, jsonify, request

import db

app = Flask(__name__)
app.config["DB_USERNAME"] = os.environ["DB_USERNAME"]
app.config["DB_PASSWORD"] = os.environ["DB_PASSWORD"]
app.config["DB_HOST"] = os.environ["DB_HOST"]
app.config["DB_PORT"] = os.environ["DB_PORT"]
app.config["DB_NAME"] = os.environ["DB_NAME"]

app.config["ENGINE"] = db.create_engine(
    dialect="postgresql",
    driver="psycopg2",
    password=app.config["DB_PASSWORD"],
    host=app.config["DB_HOST"],
    username=app.config["DB_USERNAME"],
    port=app.config["DB_PORT"],
    dbname=app.config["DB_NAME"],
)


@app.route("/api/register/<string:user_name>", methods=["GET"])
def register_user(user_name):
    status = db.register_user(app.config["ENGINE"], user_name)
    if status is None:
        return "This user name is used already.", 412
    else:
        return (
            jsonify(
                {
                    "token": status,
                }
            ),
            200,
        )


@app.route("/api/<string:user_name>", methods=["POST"])
def register_work_time(user_name):
    post_data = request.json
    if post_data is None:
        return "invalid", 403
    print(f"[DEBUG] {post_data=}")
    today = date.today()
    try:
        db.update(app.config["ENGINE"], user_name, post_data["body"], day=today)
    except db.UserNotFoundError:
        "The user is not found.", 404
    except db.InvalidTokenError:
        "The token is invalid.", 403
    return "", 200


@app.route("/api/<string:user_name>", methods=["GET"])
def get_recent_week_data(user_name):
    seven_days = db.get_recent_week(app.config["ENGINE"], user_name)
    return jsonify(seven_days), 200


@app.route("/api/<user_name>/<string:filetype>", methods=["GET"])
def get_recent_week_data_with_filetype(user_name, filetype):
    seven_days = db.get_recent_week(app.config["ENGINE"], user_name)
    return jsonify([d.get(filetype, {}) for d in seven_days]), 200


if __name__ == "__main__":
    # engine = db.create_engine(
    #     dialect="sqlite",
    #     password="",
    #     host="",
    #     username="",
    #     port="",
    #     dbname="",
    #     driver="",
    # )
    db.initialize(app.config["ENGINE"])
    app.run(debug=True)
