import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

# Load .env variables
load_dotenv()

db = SQLAlchemy()

class Config:
    # Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY", "deepali_secret")

    # JWT Configuration
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH", "private.pem")
    JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", "public.pem")

    # Load private/public keys safely
    try:
        with open(JWT_PRIVATE_KEY_PATH, "r") as f:
            JWT_PRIVATE_KEY = f.read()
    except FileNotFoundError:
        JWT_PRIVATE_KEY = None
        print(f"[ERROR] Private key file not found at {JWT_PRIVATE_KEY_PATH}")

    try:
        with open(JWT_PUBLIC_KEY_PATH, "r") as f:
            JWT_PUBLIC_KEY = f.read()
    except FileNotFoundError:
        JWT_PUBLIC_KEY = None
        print(f"[ERROR] Public key file not found at {JWT_PUBLIC_KEY_PATH}")

    # ===== DATABASE CONFIG =====
    DATABASE_URL = os.getenv("DATABASE_URL")  # Render ke liye
    if DATABASE_URL:
        # Render / URL-based Postgres
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        engine = create_engine(
            SQLALCHEMY_DATABASE_URI,
            connect_args={"sslmode": "require"}  # Render me SSL required
        )
    else:
        # Local fallback
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_NAME = os.getenv("DB_NAME", "tm")
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "Admin123")
        DB_PORT = os.getenv("DB_PORT", "5432")

        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)  # Local SSL optional

# ===== Raw psycopg2 connection function =====
def get_db_connection():
    """
    Returns a psycopg2 connection and cursor
    """
    try:
        if os.getenv("DATABASE_URL"):
            # Render / URL-based Postgres
            conn = psycopg2.connect(
                os.getenv("DATABASE_URL"),
                sslmode="require"
            )
        else:
            # Local fallback
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "tm"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "Admin123"),
                port=os.getenv("DB_PORT", "5432")
            )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("[DB ERROR]", e)
        return None, None

# ===== Quick test =====
if __name__ == "__main__":
    conn, cur = get_db_connection()
    if conn:
        print("DB CONNECTED ✅")
    else:
        print("DB FAILED ❌")
