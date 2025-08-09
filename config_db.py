import os
import psycopg2
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


class Config:
    # Secret Key (used in session or fallback)
    SECRET_KEY = os.getenv("SECRET_KEY", "deepali_secret")

    # JWT Configuration
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")

    private_key_path = os.getenv("JWT_PRIVATE_KEY_PATH", "private.pem")
    public_key_path = os.getenv("JWT_PUBLIC_KEY_PATH", "public.pem")

    # Safely load private/public keys
    try:
        with open(private_key_path, "r") as f:
            JWT_PRIVATE_KEY = f.read()
    except FileNotFoundError:
        JWT_PRIVATE_KEY = None
        print(f"[ERROR] Private key file not found at {private_key_path}")

    try:
        with open(public_key_path, "r") as f:
            JWT_PUBLIC_KEY = f.read()
    except FileNotFoundError:
        JWT_PUBLIC_KEY = None
        print(f"[ERROR] Public key file not found at {public_key_path}")

    # Database configuration (fallback to PG* if DB_* not found)
    DB_HOST = os.getenv("DB_HOST", os.getenv("PGHOST", "localhost"))
    DB_NAME = os.getenv("DB_NAME", os.getenv("PGDATABASE", "tm"))
    DB_USER = os.getenv("DB_USER", os.getenv("PGUSER", "postgres"))
    DB_PASSWORD = os.getenv("DB_PASSWORD", os.getenv("PGPASSWORD", "postgres"))
    DB_PORT = os.getenv("DB_PORT", os.getenv("PGPORT", "5432"))


# DB Connection Function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("[DB ERROR]", e)
        return None, None
