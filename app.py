from flask import Flask
from src import extraction_routes

app = Flask(__name__)
app.register_blueprint(extraction_routes)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
