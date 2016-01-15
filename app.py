# coding=utf-8
from gandalf import create_app
from gandalf.config import HOST, PORT, DEBUG
app = create_app()


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
