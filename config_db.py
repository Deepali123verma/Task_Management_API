import os
import psycopg2
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()


class Config:
    # ================= SECRET KEY =================
    SECRET_KEY = os.getenv("SECRET_KEY", "deepali_secret")

    # ================= JWT CONFIG =================
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH", "private.pem")
    JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", "public.pem")

    # Load private key
    try:
        with open(JWT_PRIVATE_KEY_PATH, "r") as f:
            JWT_PRIVATE_KEY = f.read()
    except FileNotFoundError:
        JWT_PRIVATE_KEY = None
        print(f"[ERROR] Private key not found at {JWT_PRIVATE_KEY_PATH}")

    # Load public key
    try:
        with open(JWT_PUBLIC_KEY_PATH, "r") as f:
            JWT_PUBLIC_KEY = f.read()
    except FileNotFoundError:
        JWT_PUBLIC_KEY = None
        print(f"[ERROR] Public key not found at {JWT_PUBLIC_KEY_PATH}")

    # ================= DATABASE CONFIG =================
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # For Render or deployed PostgreSQL
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"sslmode": "require"}
        }
    else:
        # Local PostgreSQL
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_NAME = os.getenv("DB_NAME", "tm")
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "Admin123")
        DB_PORT = os.getenv("DB_PORT", "5432")

        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


# ===== Raw psycopg2 connection (optional if needed) =====
def get_db_connection():
    try:
        if os.getenv("DATABASE_URL"):
            conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "tm"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "Admin123"),
                port=os.getenv("DB_PORT", "5432"),
            )
        return conn, conn.cursor()
    except Exception as e:
        print("[DB ERROR]", e)
        return None, None
