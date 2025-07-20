import psycopg2

class Config:
    SECRET_KEY = "deepali_secret"
    JWT_SECRET_KEY = "jwt_deepali_secret_123"

    DB_HOST = "localhost"
    DB_NAME = "tm"
    DB_USER = "postgres"
    DB_PASSWORD = "Admin123"
    DB_PORT = "5432"

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
        print("Database connection failed:", e)
        return None, None
