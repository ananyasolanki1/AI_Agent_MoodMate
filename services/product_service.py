import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    # Connect to the MySQL database using environment variables
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "localhost"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE", "moodmate")
    )


def get_product(product_name):
    # Find a product by name
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE LOWER(product_name) = LOWER(%s)
        """,
        (product_name,)
    )

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    # Return None if the product doesn't exist
    return product


def get_similar_price_products(product_name, price):
    # Find phones within ±20% of the current phone's price
    lower_price = price * 0.80
    upper_price = price * 1.20

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE price BETWEEN %s AND %s
        AND LOWER(product_name) != LOWER(%s)
        ORDER BY ABS(price - %s)
        LIMIT 8
        """,
        (lower_price, upper_price, product_name, price)
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


def get_all_products():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT product_name FROM products ORDER BY product_name"
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return [product["product_name"] for product in products]