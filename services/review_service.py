import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def clean_rating(rating):
    # Extract the numeric rating from text like "3.0 out of 5 stars"
    if isinstance(rating, str):
        return float(rating.split()[0])

    return float(rating)

def get_connection():
    # Connect to the MoodMate database
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="moodmate"
    )


def save_review(
    product_name,
    review_title,
    rating,
    category,
    comments,
    sentiment,
    emotion,
    suggestion_1,
    suggestion_2,
    message
):
    # Open a database connection
    connection = get_connection()
    cursor = connection.cursor()

    rating = clean_rating(rating)

    # Get the database ID of the reviewed phone
    cursor.execute(
        """
        SELECT id FROM products
        WHERE LOWER(product_name) = LOWER(%s)
        """,
        (product_name,)
    )

    product = cursor.fetchone()

    if product is None:
        cursor.close()
        connection.close()
        return

    product_id = product[0]

    # Get IDs of the recommended phones
    cursor.execute(
        "SELECT id FROM products WHERE product_name = %s",
        (suggestion_1,)
    )
    suggestion_1_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT id FROM products WHERE product_name = %s",
        (suggestion_2,)
    )
    suggestion_2_id = cursor.fetchone()[0]

    # Save the complete review and analysis
    cursor.execute(
        """
        INSERT INTO reviews
        (
            product_id,
            review_title,
            rating,
            category,
            comments,
            sentiment,
            emotion,
            suggestion_1_id,
            suggestion_2_id,
            recommendation_message
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            product_id,
            review_title,
            rating,
            category,
            comments,
            sentiment,
            emotion,
            suggestion_1_id,
            suggestion_2_id,
            message
        )
    )

    # Permanently save the changes
    connection.commit()

    cursor.close()
    connection.close()