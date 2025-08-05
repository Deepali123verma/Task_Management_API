from config_db import Config
from routes import routes

#  Create an instance of Config
config = Config()

app = Flask(__name__)

#  Set Flask config values using the instance attributes
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["JWT_ALGORITHM"] = config.JWT_ALGORITHM
app.config["JWT_PRIVATE_KEY"] = config.JWT_PRIVATE_KEY
app.config["JWT_PUBLIC_KEY"] = config.JWT_PUBLIC_KEY

jwt = JWTManager(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
