from flask import Flask
from flask_jwt_extended import JWTManager
from config_db import Config
from routes import routes  # Make sure your Blueprint is in routes.py

# Create config instance
config = Config()

# Create Flask app
app = Flask(__name__)

# Load config values from instance
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["JWT_ALGORITHM"] = config.JWT_ALGORITHM
app.config["JWT_PRIVATE_KEY"] = config.JWT_PRIVATE_KEY
app.config["JWT_PUBLIC_KEY"] = config.JWT_PUBLIC_KEY

# Initialize JWT
jwt = JWTManager(app)

# Register routes via blueprint
app.register_blueprint(routes)

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
