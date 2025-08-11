from flask import Flask
from flask_jwt_extended import JWTManager
from config_db import Config
from routes import routes
from flasgger import Swagger

app = Flask(__name__)

# JWT Configuration
app.config["JWT_ALGORITHM"] = Config.JWT_ALGORITHM
app.config["JWT_PRIVATE_KEY"] = Config.JWT_PRIVATE_KEY
app.config["JWT_PUBLIC_KEY"] = Config.JWT_PUBLIC_KEY

jwt = JWTManager(app)

# Swagger Configuration
swagger_template = {
    "info": {
        "title": "Task Management API",
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

if __name__ == '__main__':  # fixed from '_main_' to '__main__'
    app.run(debug=True)
