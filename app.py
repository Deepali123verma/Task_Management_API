from flask import Flask
from flask_jwt_extended import JWTManager
from config_db import Config
from routes import routes

app = Flask(__name__)

# JWT Configuration
app.config["JWT_ALGORITHM"] = Config.JWT_ALGORITHM
app.config["JWT_PRIVATE_KEY"] = Config.JWT_PRIVATE_KEY
app.config["JWT_PUBLIC_KEY"] = Config.JWT_PUBLIC_KEY

jwt = JWTManager(app)

# Register routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)


