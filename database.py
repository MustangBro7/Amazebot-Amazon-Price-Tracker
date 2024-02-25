# import mysql.connector
# from dotenv import load_dotenv
# import os
# # try:
# load_dotenv()
# print(os.getenv('DB_HOST'))
# mydb = mysql.connector.connect(
#     host = os.getenv('DB_HOST'),
#     user = os.getenv('DB_USER'),
#     password = os.getenv('DB_PASSWORD'),
#     database = os.getenv('DB_NAME'),

# )
# # except mysql.connector.Error as err:
#     # print(f"Error connecting to the database: {err}")

# mycursor = mydb.cursor()
 
# mycursor.execute("SHOW TABLES LIKE 'amazebot_data'")
# if mycursor.fetchone(): 
#     print("Table already exists")
# else:
#     mycursor.execute("""CREATE TABLE amazebot_data (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         price VARCHAR(255) NOT NULL,
#         name VARCHAR(255) NOT NULL,
#         link VARCHAR(2550) NOT NULL,
#         img_link VARCHAR(2550) NOT NULL
#     )""")
    

# def insert_data(display_price, product_name, url, img_src):
#     sql="INSERT INTO amazebot_data (price , name , link , img_link) VALUES (%s,%s,%s,%s)"
#     val = (display_price, product_name, url, img_src)
#     mycursor.execute(sql,val)
#     mydb.commit()   
#     print(mycursor.rowcount , "record inserted")

# def update_data(display_price, product_name, url, img_src):
#     mycursor.execute("SELECT * FROM amazebot_data WHERE link = %s",(url,))
#     # set update funcntion for price here
#     existing_record = mycursor.fetchone()
#     if existing_record:
#         print(existing_record)
#         mycursor.execute("UPDATE amazebot_data SET price = %s WHERE link = %s",(display_price , url))
#         mydb.commit()
#         return existing_record
#     else:
#         insert_data(display_price, product_name, url, img_src)

# def get_data():
#     mycursor.execute("SELECT * FROM amazebot_data")
#     data = mycursor.fetchall()
#     print(data)
#     return data

# def delete_data(link):
#     mycursor.execute("DELETE FROM amazebot_data WHERE link = %s",(link,))
#     mydb.commit()


import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to PostgreSQL database
mydb = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT', 5432)
)

# Create cursor
my_cursor = mydb.cursor()

# Check if table already exists
# my_cursor.execute("SELECT EXISTS ( SELECT * FROM information_schema.tables WHERE table_name = 'amazebot_data');")
# mydb.commit()
# if my_cursor.fetchall():
#     print("Table 'amazebot_data' already exists")
# else:
    # Create table if it doesn't exist
# my_cursor.execute("""
#     CREATE TABLE amazebot_data (
#         id SERIAL PRIMARY KEY,
#         price VARCHAR(255) NOT NULL,
#         name VARCHAR(255) NOT NULL,
#         link VARCHAR(2550) NOT NULL,
#         img_link VARCHAR(2550) NOT NULL
#     )
# """)


def insert_data(display_price, product_name, url, img_src):
    sql = "INSERT INTO amazebot_data (price, name, link, img_link) VALUES (%s, %s, %s, %s)"
    val = (display_price, product_name, url, img_src)
    my_cursor.execute(sql, val)
    mydb.commit()
    print(my_cursor.rowcount, "record inserted")

def update_data(display_price, product_name, url, img_src):
    my_cursor.execute("SELECT * FROM amazebot_data WHERE link = %s", (url,))
    existing_record = my_cursor.fetchone()
    if existing_record:
        print(existing_record)
        my_cursor.execute("UPDATE amazebot_data SET price = %s WHERE link = %s", (display_price, url))
        mydb.commit()
        return existing_record
    else:
        insert_data(display_price, product_name, url, img_src)

def get_data():
    my_cursor.execute("SELECT * FROM amazebot_data")
    data = my_cursor.fetchall()
    print(data)
    return data

def delete_data(link):
    my_cursor.execute("DELETE FROM amazebot_data WHERE link = %s", (link,))
    mydb.commit()

# Example usage
# insert_data("$29.99", "Cool Product", "https://example.com/product", "https://example.com/product.jpg")
# update_data("$34.99", "Updated Name", "https://example.com/product", "")
# get_data()
# delete_data("https://example.com/product")
