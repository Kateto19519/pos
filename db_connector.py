import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=8111,
    database="pos_system"
)


# mycursor = mydb.cursor()
# mycursor.execute('SELECT * FROM food_category')
#
# categories= mycursor.fetchall()
# print(categories)
# for category in categories:
#     print(category)
#     print("Name: "+ category[1])
