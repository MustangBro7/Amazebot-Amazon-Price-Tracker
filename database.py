import mysql.connector

try:
    mydb = mysql.connector.connect(
        host = "bhztyhjdujrstsy22vqc-mysql.services.clever-cloud.com",
        user = "uuvftx1sn4wxnxsj",
        password = "bAZQDRqlGtMlZT60xAfY",
        database = "bhztyhjdujrstsy22vqc"
    )
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")

mycursor = mydb.cursor()
 
mycursor.execute("SHOW TABLES LIKE 'amazebot_data'")
if mycursor.fetchone(): 
    print("Table already exists")
else:
    mycursor.execute("""CREATE TABLE amazebot_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        price VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        link VARCHAR(2550) NOT NULL,
        img_link VARCHAR(2550) NOT NULL
    )""")
    

def insert_data(display_price, product_name, url, img_src):
    sql="INSERT INTO amazebot_data (price , name , link , img_link) VALUES (%s,%s,%s,%s)"
    val = (display_price, product_name, url, img_src)
    mycursor.execute(sql,val)
    mydb.commit()   
    print(mycursor.rowcount , "record inserted")

def update_data(display_price, product_name, url, img_src):
    mycursor.execute("SELECT * FROM amazebot_data WHERE link = %s",(url,))
    # set update funcntion for price here
    existing_record = mycursor.fetchone()
    if existing_record:
        print(existing_record)
        mycursor.execute("UPDATE amazebot_data SET price = %s WHERE link = %s",(display_price , url))
        mydb.commit()
        return existing_record
    else:
        insert_data(display_price, product_name, url, img_src)

def get_data():
    mycursor.execute("SELECT * FROM amazebot_data")
    data = mycursor.fetchall()
    print(data)
    return data

def delete_data(link):
    mycursor.execute("DELETE FROM amazebot_data WHERE link = %s",(link,))
    mydb.commit()
