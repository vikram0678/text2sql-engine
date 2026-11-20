import os
import psycopg2 as psql
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file




def get_connection():
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]
    missing_variables=[
        variable for variable in required_variables if not os.getenv(variable)
    ]

    if missing_variables:
        raise ValueError(
            f"Missing environment variable: {', '.join(missing_variables)}"
        )
    connection = psql.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return connection



def close_connection(connection):
    if connection:
        connection.close()

def execute_query(query, params=None, fetch=True):
    connection = None
    
    try:
        connection = get_connection()

        with connection:
            with connection.cursor() as cursor:

                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                return cursor.rowcount
    except psql.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        close_connection(connection)
    def test_fetch_false(self):
        """Test row count returned when fetch is False."""

        query = """
        SELECT customer_id, name, region
        FROM customers
        ORDER BY customer_id
        LIMIT 5;
        """

        result = execute_query(query, fetch=False)

        self.assertEqual(result, 5)