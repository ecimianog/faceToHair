import sqlite3
import os

sqliteConnection = sqlite3.connect('pre.db')
cursor = sqliteConnection.cursor()


def createDataBase():
    # SQL create a table in the database
    sql_command = """CREATE TABLE decisions ( 
    lineHA INTEGER,
    lineHB INTEGER,
    lineHC INTEGER,
    lineHD INTEGER,
    lineVA INTEGER,
    lineVB INTEGER,
    lineVC INTEGER,
    lineVD INTEGER,
    modelSelected INTEGER, 
    date INTEGER);"""

    cursor.execute(sql_command)


def insertDecision(listPoints, model):
    valuesString = False
    for l in listPoints:
        if valuesString:
            valuesString = f"{valuesString}, '{l}'"
        else:
            valuesString = f"'{l}'"
    try:
        cursor.execute(
            f"INSERT INTO listasBorrar VALUES ('{valuesString}', '{title}', {model})")
    except:
        print('Error inserting values in DB.')
    sqliteConnection.commit()


# createDataBase()
# close the connection
sqliteConnection.close()