import os
import psycopg2
from dotenv import load_dotenv
from functools import wraps
from logger import logger


load_dotenv()


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            db_config = {
            "dbname":   os.getenv("DB_NAME"),
            "user":     os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host":     os.getenv("DB_HOST"),
            "port":     os.getenv("DB_PORT")
            }                  

            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            logger.info("DB connection established for function '%s'", func.__name__)

            result = func(*args, cursor=cursor, **kwargs)

            conn.commit()
            cursor.close()
            conn.close()
            logger.info("DB connection closed for function '%s'", func.__name__)

            return result

        except Exception as e:
            logger.error("Error in DB connection for function '%s': %s", func.__name__, e)
            return {"status": "fail", "message": str(e)}

    return wrapper
