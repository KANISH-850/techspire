import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def create_database():
    try:
        # Connect to postgres db to create the new db
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.DATABASE_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database {settings.DATABASE_NAME}...")
            cursor.execute(f'CREATE DATABASE "{settings.DATABASE_NAME}"')
            print("Database created successfully.")
        else:
            print(f"Database {settings.DATABASE_NAME} already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
