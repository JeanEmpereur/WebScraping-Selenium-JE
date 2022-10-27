import mysql.connector

class Database:
    def connectDb():
        mydb = mysql.connector.connect(
            host="localhost",
            user="redpanda",
            password="redpanda",
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS animes")

    def createTable():
        mydb = mysql.connector.connect(
            host="localhost",
            user="redpanda",
            password="redpanda",
            database="animes",
        )
        mycursor = mydb.cursor()
        mycursor.execute("DROP TABLE IF EXISTS anime")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS anime ("
            "img VARCHAR(255), "
            "name VARCHAR(255), "
            "nb_avis INTEGER, "
            "note FLOAT, "
            "nb_votant INTEGER, "
            "production VARCHAR(255), "
            "tags VARCHAR(255), "
            "description VARCHAR(2000))"
        )

    def addRow(item):
        mydb = mysql.connector.connect(
            host="localhost",
            user="redpanda",
            password="redpanda",
            database="animes",
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO anime (name, img, nb_avis, note, nb_votant, description, tags, production) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            item['name'], 
            item['image'], 
            item['nb_avis'], 
            item['note'], 
            item['nb_votant'],
            item['description'],
            item['tags'],
            item['production'])
        mycursor.execute(sql, val)
        mydb.commit()
