import shelve
from uuid import uuid4

from flask import Flask, request, jsonify

from imgurpython import ImgurClient
from imgurconf import CLIENT_ID, CLIENT_SECRET

import traceback
import logging
logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

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


# curl -H "Content-Type: application/json" -X POST -d
# '{"uuid" : "33", "media_uri":"random"}' http://localhost:5000/store/
@app.route('/store/', methods=['POST'])
def local_save_image():

    if 'uuid' in request.json and 'media_uri' in request.json:

        uuid = request.json['uuid']
        media_uri = request.json['media_uri']

        db = open_db()

        if uuid in db:
            db[uuid] = {'media_uri': media_uri}
            imgur_link = imgur_save_image(media_uri)
            save_to_file(imgur_link) if imgur_link else None

            return jsonify(status=True,
                           message="Media stored",
                           imgur_link=imgur_link)
        else:
            return jsonify(status=False, message="GTFO")

    else:
        return jsonify(status=False, message="Bad Data")


# Send to a private album in imgur
def imgur_save_image(image_path):

    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    client = ImgurClient(client_id, client_secret)

    try:
        image_json = client.upload_from_path(image_path,
                                             config=None,
                                             anon=True)
        link = image_json['link']
        logging.info('Image saved in imgur: {0}'.format(link))
        return link

    except:
        logging.error('Error trying to connect to imgur.')
        logging.error(traceback.format_exc())
        return None


def save_to_file(link):
    try:
        f = open('imgur.txt', 'a')
        f.write('{0} \n'.format(link))
        f.close()
        logging.info('Link saved to file.')

    except:
        logging.error('Error trying to write to file. Skipping it.')
        logging.error(traceback.format_exc())
        return None


if __name__ == '__main__':
    app.run(debug=True)
