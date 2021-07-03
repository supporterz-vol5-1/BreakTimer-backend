from datetime import date

from flask import Flask, jsonify, request

import db

app = Flask(__name__)


@app.route("/start/<string:user_id>", methods=["POST"])
def store(user_id):
    post_data = request.json
    today = date.today()
    db.update(engine, user_id, post_data, day=today)
    return "", 200


@app.route("/api/<string:user_id>", methods=["GET"])
def get_recent_week_data(user_id):
    seven_days = db.get_recent_week(engine, user_id)
    return jsonify(seven_days)


@app.route("/api/<user_id>/<language>", methods=["GET"])
def get_recent_week_data_with_language(user_id, language):
    pass


if __name__ == "__main__":
    engine = db.create_engine(
        dialect="sqlite",
        password="",
        host="",
        username="",
        port="",
        dbname="",
        driver="",
    )
    db.initialize(engine)
    app.run(debug=True)
