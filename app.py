from flask import Flask

app = Flask(__name__)


@app.route("/start/<user_id>", methods="POST")
def start(user_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
