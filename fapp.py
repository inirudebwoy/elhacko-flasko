import shelve
from uuid import uuid4

from flask import Flask, request


app = Flask(__name__)
DB_PATH = 'db.shelve'


def open_db():
    return shelve.open(DB_PATH)


def generate_uuid_hex():
    uuid = uuid4().hex
    db = open_db()

    if uuid in db:
        return generate_uuid_hex()

    # create bucket for UUID
    db[uuid] = {}

    db.close()
    return uuid


@app.route('/uuid')
def get_uuid():
    return generate_uuid_hex()


@app.route('/store/', methods=['POST'])
def store_image():

    uuid = request.form["uuid"]
    media_uri = request.form["media_uri"]

    if uuid and media_uri:
        db = open_db()
        if uuid in db:
            db[uuid] = {"media_uri":media_uri}
            return {"status": True, "message": "Media stored"}
        else:
            return {"status": False, "message": "GTFO"}
    else:
        return {"status": False, "message": "Bad Data"}

if __name__ == '__main__':
    app.run(debug=True)
