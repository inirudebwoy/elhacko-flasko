import shelve
from uuid import uuid4

from flask import Flask, request, jsonify

from imgurpython import ImgurClient
from imgur.imgurconf import CLIENT_ID, CLIENT_SECRET
from imgur.imgurtokens import ACCESS_TOKEN, REFRESH_TOKEN
from imgur.albumhash import ALBUM_ID

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
            image_json = imgur_save_image_anonymously(media_uri)
            imgur_save_image_to_users_account(image_json['id'])
            save_to_file(image_json['link']) if image_json['link'] else None

            return jsonify(status=True,
                           message="Media stored",
                           imgur_link=image_json['link'])
        else:
            return jsonify(status=False, message="GTFO")

    else:
        return jsonify(status=False, message="Bad Data")


# Store anonimously in imgur
def imgur_save_image_anonymously(image_path):

    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    client = ImgurClient(client_id, client_secret)

    try:
        image_json = client.upload_from_path(image_path,
                                             config=None,
                                             anon=True)
        logging.info('Image saved in imgur: {0}'.format(image_json['link']))
        return image_json

    except:
        logging.error('Error trying to connect to imgur. (Image save)')
        logging.error(traceback.format_exc())
        return None


# Send to a private album of your user in imgur
def imgur_save_image_to_users_account(image_id):

    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    access_token = ACCESS_TOKEN
    refresh_token = REFRESH_TOKEN

    client = ImgurClient(client_id, client_secret, access_token, refresh_token)

    try:
        client.album_add_images(ALBUM_ID, [image_id])

        logging.info('Image saved in album')

    except:
        logging.error('Error trying to connect to imgur. (Album save)')
        logging.error(traceback.format_exc())
        return None


def save_to_file(link):
    try:
        f = open('imgur/imgur.txt', 'a')
        f.write('{0} \n'.format(link))
        f.close()
        logging.info('Link saved to file.')

    except:
        logging.error('Error trying to write to file. Skipping it.')
        logging.error(traceback.format_exc())
        return None


if __name__ == '__main__':
    app.run(debug=True)
