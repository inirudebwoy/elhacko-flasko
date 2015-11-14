from uuid import uuid4

from flask import Flask


app = Flask(__name__)


@app.route('/')
def generate_uuid():
    uuid = uuid4()
    return uuid.hex


if __name__ == '__main__':
    app.run(debug=True)
