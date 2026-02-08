import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()

db = SQLAlchemy()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "deepali_secret")

    # JWT Configuration
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH", "private.pem")
    JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", "public.pem")

    # Safely load private/public keys
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

    # DATABASE_URL from Render env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # SSL required for Render Postgres
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        connect_args={"sslmode": "require"}
    )


def get_db_connection():
    """Direct psycopg2 connection (optional for raw SQL queries)"""
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            sslmode="require"
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("[DB ERROR]", e)
        return None, None
