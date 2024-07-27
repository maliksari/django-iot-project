import psycopg2
import logging
import os

from datetime import datetime
from psycopg2 import sql
from dotenv import load_dotenv


load_dotenv()


DATABASE = {
    'dbname': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT'),
}


logger = logging.basicConfig(
    filename='tcp_celery.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def save_location_to_db(device_id, latitude, longitude):
    try:
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        now = datetime.now()

        query = sql.SQL("""
            INSERT INTO location (device_id, latitude, longitude, created_on,
                        modified_on, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)

        cur.execute(query, (device_id, latitude, longitude, now, now, True))
        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        logger.error(f"Error saving location to database: {e}")
