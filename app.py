from flask import Flask
from src import flask_adapter
from src import st_init

st_init()

# or

# app = Flask(__name__)
# app.register_blueprint(flask_adapter)

# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=8000)
