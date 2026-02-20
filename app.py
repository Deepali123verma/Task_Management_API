from flask import Flask
from flask_jwt_extended import JWTManager
from config_db import Config, db
from routes import routes
from flasgger import Swagger


app = Flask(__name__)

# Load ALL configuration from Config class
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Create tables
with app.app_context():
    db.create_all()

# Swagger Configuration
swagger_template = {
    "info": {
        "title": "Task Management System",
        "description": "API documentation for the Task Management project with JWT authentication, role-based authorization, and encryption.",
        "version": "1.0.0",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [{"Bearer": []}],
}

swagger = Swagger(app, template=swagger_template)

# Register routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
