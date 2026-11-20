import psycopg2

import unittest
from src.db import execute_query, get_connection

class TestDatabaseLifecycle(unittest.TestCase):

    def setUp(self):
        # Open one database connection for this test.
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

        # Create a temporary table for testing.
        self.cursor.execute("""
            CREATE TEMP TABLE test_customers (
                customer_id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)

        # Insert temporary test data.
        self.cursor.execute("""
            INSERT INTO test_customers (customer_id, name)
            VALUES (%s, %s);
        """, (999999, "Test Customer"))

    def test_invalid_query(self):
        """Test whether database errors are raised for invalid SQL."""

        query = """
        SELECT * FROM invalid_table_name;
        """

        with self.assertRaises(psycopg2.Error):
            execute_query(query)


    def test_fetch_false(self):
        """Test whether execute_query returns row count when fetch is False."""

        query = """
        SELECT customer_id, name, region
        FROM customers
        ORDER BY customer_id
        LIMIT 5;
        """

        result = execute_query(query, fetch=False)

        self.assertEqual(result, 5)

        
    def test_parameterized_query(self):
        """Test filtering customers using a SQL parameter."""

        query = """
        SELECT customer_id, name, region
        FROM customers
        WHERE region = %s
        ORDER BY customer_id
        LIMIT 5;
        """

        results = execute_query(query, params=("West",))

        self.assertGreater(len(results), 0)

        self.assertLessEqual(len(results), 5)

        for row in results:
            self.assertEqual(row[2], "West")
    def test_temporary_customer(self):
        self.cursor.execute("""
            SELECT customer_id, name
            FROM test_customers;
        """)

        result = self.cursor.fetchone()

        self.assertEqual(result, (999999, "Test Customer"))

    def tearDown(self):
        # Undo database changes.
        self.connection.rollback()

        # Close database resources.
        self.cursor.close()
        self.connection.close()


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