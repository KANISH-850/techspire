import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "5432")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DB_NAME = os.getenv("DATABASE_NAME", "ceo_dashboard")


def create_database():
    try:
        # Connect to the default PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check whether the database already exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (DB_NAME,)
        )

        exists = cursor.fetchone()

        if not exists:
            print(f"Creating database {DB_NAME}...")
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print("Database created successfully!")
        else:
            print(f"Database {DB_NAME} already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")


if __name__ == "__main__":
    create_database()