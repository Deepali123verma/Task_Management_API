import os
import psycopg2
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class Config:
    def __init__(self):
        # General Configuration
        self.SECRET_KEY = os.getenv("SECRET_KEY", "deepali_secret")

        # JWT Configuration
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
        private_key_path = os.getenv("JWT_PRIVATE_KEY_PATH", "private.pem")
        public_key_path = os.getenv("JWT_PUBLIC_KEY_PATH", "public.pem")

        # Load private key
        try:
            with open(private_key_path, "r") as f:
                self.JWT_PRIVATE_KEY = f.read()
        except FileNotFoundError:
            self.JWT_PRIVATE_KEY = None
            print(f"[ERROR] Private key file not found at {private_key_path}")

        # Load public key
        try:
            with open(public_key_path, "r") as f:
                self.JWT_PUBLIC_KEY = f.read()
        except FileNotFoundError:
            self.JWT_PUBLIC_KEY = None
            print(f"[ERROR] Public key file not found at {public_key_path}")

        # Database Configuration
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_NAME = os.getenv("DB_NAME", "tm")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
        self.DB_PORT = os.getenv("DB_PORT", "5432")


# DB Connection Function
def get_db_connection(config: Config = Config()):
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("[DB ERROR]", e)
        return None, None
