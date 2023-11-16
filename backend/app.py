from flask import Flask
from app_routes import extraction_routes

app = Flask(__name__)
app.register_blueprint(extraction_routes)

if __name__ == "__main__":
    app.run(debug=True)
