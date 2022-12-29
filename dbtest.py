import dbconfig as dbcg
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE Librarian")
mycursor.execute("SHOW DATABASES")

for db in mycursor:
    if db == ('librarian',):
        create = 0

create = any(db for db in mycursor if db == ('librarian',))

if not create:
    mycursor.execute("CREATE DATABASE Librarian")
