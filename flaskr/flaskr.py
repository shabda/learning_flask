import sqlite3
from contextlib import closing

from flask import Flask, g

DATABASE = "data.db"
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config["DATABASE"])


@app.before_request
def get_db():
    g.db = connect_db()


@app.teardown_request
def close_db(exception):
    g.db.close()


@app.route('/')
def hello():
    return "Hello World"

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource("schema.sql") as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == "__main__":
    app.run()
