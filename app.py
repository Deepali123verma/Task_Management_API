from flask import Flask
from flask_jwt_extended import JWTManager
from config_db import Config
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(routes)

@app.route('/')
def home():
    return "Flask App with JWT is Running!"

if __name__ == '__main__':
    app.run(debug=True)


