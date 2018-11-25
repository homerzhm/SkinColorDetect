from api import app
from os import environ


if __name__ == '__main__':
    port = 8001
    hostname = environ.get('SERVER_HOST', 'localhost')
    app.run(host='127.0.0.1', port=port, debug=True)
