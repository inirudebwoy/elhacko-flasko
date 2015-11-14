import shelve
from uuid import uuid4

from flask import Flask, request, jsonify


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


# curl -X GET "http://localhost:5000/media_uri/?uuid=33"
@app.route('/media_uri/', methods=['GET'])
def get_media_uri():
    uuid = request.args.get("uuid", None)
    db = open_db()
    if uuid and uuid in db and db[uuid]:
        media_uri = db[uuid]['media_uri']
        return jsonify(status=True, uuid=uuid, media_uri=media_uri)
    else:
        return jsonify(status=False, uuid=uuid, media_uri=None)


# curl -H "Content-Type: application/json" -X POST -d '{"uuid" : "33", "media_uri":"random"}' http://localhost:5000/store/
@app.route('/store/', methods=['POST'])
def store_image():

    if 'uuid' in request.json and 'media_uri' in request.json:

        uuid = request.json['uuid']
        media_uri = request.json['media_uri']

        db = open_db()
        
        if uuid in db:
            db[uuid] = {'media_uri':media_uri}
            return jsonify(status=True, message="Media stored")
        else:
            return jsonify(status=False, message="GTFO")

    else:
        return jsonify(status=False, message="Bad Data")

if __name__ == '__main__':
    app.run(debug=True)
