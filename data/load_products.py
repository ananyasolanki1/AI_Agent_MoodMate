import pandas as pd
import mysql.connector

# Load product data from CSV
df = pd.read_csv("data/mobile_details.csv")

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="moodmate"
)

cursor = connection.cursor()

# Insert each product into MySQL
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO products
        (product_name, price, display, battery, camera, processor,
         ram, storage, charging, network, key_qualities)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            row["Product Name"],
            row["Price"],
            row["Display"],
            row["Battery (mAh)"],
            row["Camera"],
            row["Processor"],
            row["RAM"],
            row["Storage"],
            row["Charging"],
            row["Network"],
            row["Key Qualities"]
        )
    )

connection.commit()

cursor.close()
connection.close()

print("Products loaded successfully!")