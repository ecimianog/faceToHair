import sqlite3
import os
import time
import numpy as np

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
    now = time.strftime("%Y%m%d_%H%M%S")
    for l in listPoints:
        if valuesString:
            valuesString = f"{valuesString}, '{l}'"
        else:
            valuesString = f"'{l}'"
    try:
        cursor.execute(
            f"INSERT INTO listasBorrar VALUES ('{valuesString}', '{now}', {model})")
    except:
        print('Error inserting values in DB.')
    sqliteConnection.commit()


def getDecision(listPoints):
    models = {'heart': ['01a', '01b', '01c'], 'ellipse': ['02a', '02b', '02c'], 'rectangle': ['03a', '03b', '03c'], 'square': [
        '04a', '04b', '04c'], 'circle': ['05a', '05b', '05c'], 'rhomb': ['06a', '06b', '06c'], }
    resultA, resultB, resultC, resultD = getRatios(listPoints)
    return models['rectangle']


def getRatios(marks):
    pAr = np.array([marks[0].x, marks[0].y, marks[0].z])
    pAl = np.array([marks[4].x, marks[4].y, marks[4].z])
    pBr = np.array([marks[1].x, marks[1].y, marks[1].z])
    pBl = np.array([marks[7].x, marks[7].y, marks[7].z])
    pCr = np.array([marks[2].x, marks[2].y, marks[2].z])
    pCl = np.array([marks[6].x, marks[6].y, marks[6].z])
    pDr = np.array([marks[3].x, marks[3].y, marks[3].z])
    pDl = np.array([marks[5].x, marks[5].y, marks[5].z])
    vA = np.array([marks[0].x, marks[0].y, marks[0].z,
                  marks[4].x, marks[4].y, marks[4].z])
    #magA = math.sqrt(sum(pow(element, 2) for element in vA))
    horizA = np.linalg.norm(pAr - pAl)
    horizB = np.linalg.norm(pBr - pBl)
    horizC = np.linalg.norm(pCr - pCl)
    horizD = np.linalg.norm(pDr - pDl)
    vertA = np.linalg.norm(pAr - pDr)
    vertB = np.linalg.norm(pAl - pDl)
    vertC = np.linalg.norm(pBr - pCl)
    vertD = np.linalg.norm(pBl - pCr)
    #magB = math.sqrt(sum(pow(element, 2) for element in vB))
    #magC = math.sqrt(sum(pow(element, 2) for element in vC))
    #magD = math.sqrt(sum(pow(element, 2) for element in vD))
    resultA = np.inner(pAr, pAl)
    resultB = np.inner(pBr, pBl)
    resultC = np.inner(pCr, pCl)
    resultD = np.inner(pDr, pDl)
    #print(resultA, resultB, resultC, resultD)
    print(horizA, horizB, horizC, horizD)
    print(vertA, vertB, vertC, vertD)
    return resultA, resultB, resultC, resultD


# createDataBase()
# close the connection
sqliteConnection.close()
