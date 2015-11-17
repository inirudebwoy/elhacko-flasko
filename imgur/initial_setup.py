from imgurpython import ImgurClient
from imgurconf import CLIENT_ID, CLIENT_SECRET, PIN
import requests

client_id = CLIENT_ID
client_secret = CLIENT_SECRET


if __name__ == '__main__':

    client = ImgurClient(client_id, client_secret)

    refresh_data = {"client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "grant_type": "pin",
                    "pin": PIN}

    r = requests.post("https://api.imgur.com/oauth2/token", data=refresh_data)

    f = open('imgurtokens.py', 'w')
    f.write('ACCESS_TOKEN = "{0}"\n'.format(r.json()['access_token']))
    f.write('REFRESH_TOKEN = "{0}"\n'.format(r.json()['refresh_token']))
    f.close()
