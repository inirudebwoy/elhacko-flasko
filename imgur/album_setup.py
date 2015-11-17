from imgurpython import ImgurClient
from imgurtokens import ACCESS_TOKEN, REFRESH_TOKEN
from imgurconf import CLIENT_ID, CLIENT_SECRET
from albumconf import ALBUM_DESCRIPTION, ALBUM_PRIVACY, ALBUM_TITLE
import traceback
import logging

# If you already have an access/refresh pair in hand
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
access_token = ACCESS_TOKEN
refresh_token = REFRESH_TOKEN

if __name__ == '__main__':

    # Note since access tokens expire after an hour
    # only the refresh token is required (library handles autorefresh)
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)

    album_fields = {'description': ALBUM_DESCRIPTION,
                    'privacy': ALBUM_PRIVACY,
                    'title': ALBUM_TITLE}

    try:
        album = client.create_album(album_fields)
        f = open('albumhash.py', 'w')
        f.write('ID = "{0}"\n'.format(album["id"]))
        f.write('HASH = "{0}"\n'.format(album["deletehash"]))
        f.close()
        print "Album created successfully"

    except:
        logging.error(traceback.format_exc())
