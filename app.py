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
    dialect="postgres",
    password=app.config["DB_PASSWORD"],
    host=app.config["DB_HOST"],
    username=app.config["DB_USERNAME"],
    port=app.config["DB_PORT"],
    dbname=app.config["DB_NAME"],
)


@app.route("/api/<string:user_id>", methods=["POST"])
def register_work_time(user_id):
    post_data = request.json
    today = date.today()
    db.update(app.config["ENGINE"], user_id, post_data, day=today)
    return "", 200


@app.route("/api/<string:user_id>", methods=["GET"])
def get_recent_week_data(user_id):
    seven_days = db.get_recent_week(app.config["ENGINE"], user_id)
    return jsonify(seven_days), 200


@app.route("/api/<user_id>/<language>", methods=["GET"])
def get_recent_week_data_with_language(user_id, language):
    pass


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
    # db.initialize(app.config["ENGINE"])
    app.run(debug=True)
